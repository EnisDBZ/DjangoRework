from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.apps import apps
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Products, CartItem, Categories,Billing , BilledItems,Resimler,CartItemQuickBuy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import admin
import json
import random
from django.core.paginator import Paginator



# Create your views here.


def categories_list(request):
    categories = Categories.get_main_categories()  # Tüm ana kategorileri al

    context = {
        'categories': categories,


    }
    return render(request, "intern_app/categories.html", context)


def categories(request, slug):
    # get_object_or_404 ile varsa Categories modelinden slug yani alan adını alıyoruz
    category = get_object_or_404(Categories, slug=slug)

    # Ürün kategorisinin yukarıdaki değişkenle aynı olanları filteliyoruz
    products = Products.objects.filter(product_category=category)
    # Categories modelindeki alt kategorileri alıyoruz
    sub_categories = category.sub_categories.all()
    context = {
        'category': category,
        'products': products,
     
    }

    return render(request, "intern_app/categories_added.html", context)

def category_products(request,slug):
    category = get_object_or_404(Categories,slug=slug)

    products = Products.objects.filter(product_category=category)

    sub_categories = category.sub_categories.all()

    context = {
        'category':category,
        'products':products,
        'sub_categories':sub_categories,
    }
    return render(request,"intern_app/subcategory_products.html",context)


def search_view(request):
    
    # GET ile arama sorgusunu alıyoruz
    search_query = request.GET.get('search_query', '')
    if search_query:
        # icontains ve contains alt dizeleri arar tek fark icontains büyük-küçük harf duyarsızdır.
        # iexact de büyük-küçük harf duyarsız tam olarak aranan kelimeyi ister. "|" ise birden çok filtrelemede kullanılır.
        posts = Products.objects.filter(
            Q(product_name__icontains=search_query) |
            Q(product_name__iexact=search_query) |
            Q(product_name__contains=search_query) 
            
        )
    else:
        posts = Products.objects.none()  # Eğer arama yapılmadıysa, boş liste döner

    return render(request, 'intern_app/search_result.html', {'query': search_query, 'posts': posts})


def index(request):
    return render(request, 'intern_app/index.html')


@login_required
def setting(request):
    return render(request, 'intern_app/setting.html')


# Authentication #

# Kullanıcı modelini alıp User değişkeni içinde saklıyoruz.
User = get_user_model()

# İsim,soyisim güncelleme fonksiyonu


def update_names(request):
    # Post methodu ile name değerleri isim ve soyisim olan inputları alıyoruz
    if request.method == 'POST':
        isim = request.POST.get('isim')
        soyisim = request.POST.get('soyisim')
        # İsmin ve soyismin uzunluğu 2 karakterden küçükse hata mesajı gösterip aynı sayfaya geri yönlendiriyoruz.
        if len(isim) < 2:
            messages.error(request, 'İsminiz en az 2 karakterli olabilir!')
            return redirect('intern_app:update_names')
        if len(soyisim) < 2:
            messages.error(request, 'Soyisminiz en az 2 karakterli olabilir!')
            return redirect('intern_app:update_names')
        # Django da auth.User olan önceden tanımlı modelin değişkenlerini request ile kendi değişkenlerimize eşitliyoruz.
        request.user.first_name = isim
        request.user.last_name = soyisim
        request.user.save()

        # Bilgileri güncelledikten sonra kullanıcının otomatik olarak çıkış yapmasını önlüyoruz
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Bilgileriniz başarıyla güncellendi!')
        return redirect('intern_app:settings')
    return render(request, 'intern_app/setting.html')

# E-posta güncelleme fonksiyonu


def update_email(request):
    # Eski ve yeni e-postalarımızı request ile alıyoruz.
    if request.method == 'POST':
        old_email = request.POST.get('old_email')
        new_email = request.POST.get('new_email')

        # Eski e-postamızın güncel e-postamız ile uyuştuğunu kontrol ediyoruz.
        if request.user.email != old_email:
            messages.error(request, 'Eski e-posta adresinizi yanlış girdiniz!')
            return redirect('intern_app:update_email')

        # Değiştirilmek istenen e-postanın başka biri tarafından kullanıp kullanılmadığını kontrol ediyoruz.
        if User.objects.filter(email=new_email).exists():
            messages.error(request, 'Bu eposta adresi zaten kullanılmakta!')
            return redirect('intern_app:update_email')

        # Eğer yeni e-posta kimse tarafından kullanılmıyorsa bunu kaydediyoruz.
        request.user.email = new_email
        request.user.save()

        # Bilgiyi güncelledikten sonra kullanıcının çıkış yapmasını önlüyoruz.
        update_session_auth_hash(request, request.user)
        messages.success(request, 'E-posta adresiniz başarıyla güncellendi!')
        return redirect('intern_app:settings')
    return render(request, 'intern_app/setting.html')

# Şifre güncelleme fonksiyonu


def update_password(request):
    # Güncel şifremiz ile yeni şifremizi request ile alıyoruz.
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        # Güncel şifremizin doğru olup olmadığını kontrol ediyoruz.
        if not request.user.check_password(old_password):
            messages.error(request, 'Eski şifrenizi yanlış girdiniz!')
            return redirect('intern_app:update_password')
        # Yeni şifremizin 8 karakterden küçük olma durumunda hata gösteriyoruz.
        if len(new_password) < 8:
            messages.error(
                request, 'Yeni şifreniz en az 8 karakter olmak zorunda!')
            return redirect("intern_app:update_password")
        # Set_password hazır fonksiyonu ile kullanıcının yeni şifresini kaydediyoruz.
        request.user.set_password(new_password)
        request.user.save()

        # Oturumu açık tutmak için
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Şifreniz başarıyla güncellendi!')
        return redirect('intern_app:settings')

    return render(request, "intern_app/setting.html")

# Giriş Yap butonu için fonksiyon


def redirect_url_(request):
    # Eğer kullanıcı giriş yapmış işe anasayfaya giriş yapmamış ise giriş sayfasına yönlendiriyor.
    if request.user.is_authenticated:
        redirect_url = 'index'
    else:
        redirect_url = 'login'

    return render(request, 'intern_app/index.html', {'redirect_url': redirect_url})

# Giriş yapma fonksiyonu


def login_view(request):
    # Django'nun hazır modeli ile kullanıcı adı ve şifreyi alıyoruz.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # Eğer kullanıcı değeri None ise Giriş ekranına yönlendiriyoruz.
        if user is not None:
            login(request, user)
            # Eğer kullanıcı yetkili ise direkt olarak yönetici paneline değil ise anasayfaya yönlendiriyoruz.
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('intern_app:yonetici-paneli')
            elif user.is_authenticated:
                return redirect('intern_app:index')

            return render(request, 'intern_app/index.html')
        else:
            return render(request, 'registration/login.html', {'error': 'Geçersiz giriş.'})

    return render(request, 'registration/login.html')

# login_required fonksyionu önceden tanımlıdır
# ve istenilen fonksiyonlara giriş yapılmadığı sürece erişim engeli getirir.


@login_required
# Çıkış yapma fonksiyonu
def logout_view(request):
    logout(request)
    # Çıkış yaptıktan sonra anasayfaya yönlendirir.
    return redirect('intern_app:index')

# Kayıt olma fonksiyonu


def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Şifrelerin eşleşip eşleşmediğini kontrol eder
        if password != confirm_password:
            messages.error(request, 'Şifreler eşleşmiyor.')
            return render(request, 'registration/signup.html')

        # Kullanıcı oluşturur. Eğer başarılıysa giriş ekranına değilse
        # kayıt ekranına hata mesajı ile beraber geri gönderir.
        try:
            user = User.objects.create_user(
                email=email, username=username, password=password)
            user.save()
            messages.success(
                request, 'Başarıyla kayıt oldunuz. Giriş yapabilirsiniz.')
            return redirect('intern_app:login')
        except Exception as e:
            messages.error(
                request, 'Kayıt olurken bir hata meydana geldi:' + str(e))

    return render(request, 'registration/signup.html')


# Authentication #

# Shopping #

# Satın alım sayfası
def shipping_checked(request):
    return render(request,"intern_app/shipped.html")

def checkout(request):
    # Kullanıcın sepetindeki ürünleri alır
    cart_items = CartItem.objects.filter(user=request.user)
    # Toplam fiyatı alır.
    total_price = sum(item.cart_name.product_price *
                      item.cart_quantity for item in cart_items)
    
    # Sipariş bilgilerini almak
    if request.method == "POST":
        #new_billing değişkenine Billing modelini atadık
        new_billing = Billing()
       
        new_billing.user = request.user
        new_billing.name = request.POST.get("isim")
        new_billing.surname = request.POST.get("soyisim")
        new_billing.email = request.POST.get("email")
        new_billing.telno = request.POST.get("telno")
        new_billing.city = request.POST.get("il")
        new_billing.town = request.POST.get("ilce")
        new_billing.zipcode = request.POST.get("zipcode")
        new_billing.address = request.POST.get("acikadres")
        new_billing.pay_method = request.POST.get("odeme")
        new_billing.card_no = request.POST.get("kartno")
        new_billing.card_exp = request.POST.get("exp")
        new_billing.card_owner = request.POST.get("kart-isim")
        new_billing.card_cvv = request.POST.get("cvc")

        new_billing.billing_total_price = total_price
 
        
        # Her bir oluşan fatura için LPF(rastgelesayi) fonksyionu
        trackno = "LPF" + str(random.randint(111111,999999))
        # TrackNo boş olduğu sürece her oluşan fatura için trackno ekleyecek
        while True:
            trackno = "LPF" + str(random.randint(111111, 999999))
            if not Billing.objects.filter(tracking_no=trackno).exists():
                new_billing.tracking_no = trackno
                break
        #trackno içeriğini değiştirip kaydediyor
        new_billing.save()


        # Sepetimizdeki ürünleri alıyoruz
        new_billing_items = CartItem.objects.filter(user=request.user)
        # Sepetimizden alınan her bir ürün için önceden oluşturulan faturanın takip numarası ile beraber 
        # fatura oluşturuyouz
        for item in new_billing_items:
            while True:
                product_no = "URN" + str(random.randint(1111111, 9999999))
                if not BilledItems.objects.filter(no=product_no).exists():
                    BilledItems.objects.create(
                        bills=new_billing,
                        product=item.cart_name,
                        no=product_no,
                        price=item.cart_name.product_price,
                        quantity=item.cart_quantity,
                    )
                    break
       

        # Satın alımdan sonra sepeti temizliyoruz.
        CartItem.objects.filter(user=request.user).delete()

        messages.success(request,"Siparişiniz başarılı bir şekilde alındı!")
        return redirect("/")
    context = {
      
        "cart_items":cart_items,
        "total_price":total_price,
    }
    return render(request,"intern_app/checkout.html",context)

def checkout_quick_buy(request,product_id):

    product = Products.objects.get(id=product_id)

    # Kullanıcın sepetindeki ürünleri alır
    user = request.user
    cart_items = CartItem.objects.filter(user=user, cart_name=product).first()

    quick_buy = CartItemQuickBuy.objects.get(user=request.user, item_name=product)

 

    
    # Sipariş bilgilerini almak
    if request.method == "POST":
        #new_billing değişkenine Billing modelini atadık
        new_billing = Billing()
       
        new_billing.user = request.user
        new_billing.name = request.POST.get("isim")
        new_billing.surname = request.POST.get("soyisim")
        new_billing.email = request.POST.get("email")
        new_billing.telno = request.POST.get("telno")
        new_billing.city = request.POST.get("il")
        new_billing.town = request.POST.get("ilce")
        new_billing.zipcode = request.POST.get("zipcode")
        new_billing.address = request.POST.get("acikadres")
        new_billing.pay_method = request.POST.get("odeme")
        new_billing.card_no = request.POST.get("kartno")
        new_billing.card_exp = request.POST.get("exp")
        new_billing.card_owner = request.POST.get("kart-isim")
        new_billing.card_cvv = request.POST.get("cvc")

        if cart_items:

            new_billing.billing_total_price = cart_items.cart_name.product_price
        else:
            new_billing.billing_total_price = quick_buy.item_name.product_price
        
        # Her bir oluşan fatura için LPF(rastgelesayi) fonksyionu
        trackno = "LPF" + str(random.randint(111111,999999))
        # TrackNo boş olduğu sürece her oluşan fatura için trackno ekleyecek
        while True:
            trackno = "LPF" + str(random.randint(111111, 999999))
            if not Billing.objects.filter(tracking_no=trackno).exists():
                new_billing.tracking_no = trackno
                break
        #trackno içeriğini değiştirip kaydediyor
        new_billing.save()


        # Sepetimizdeki ürünleri alıyoruz
        if cart_items:
            new_billing_items = CartItem.objects.filter(user=request.user)
        else:
            new_billing_items = CartItemQuickBuy.objects.filter(user=request.user)    
        # Sepetimizden alınan her bir ürün için önceden oluşturulan faturanın takip numarası ile beraber 
        # fatura oluşturuyouz
          # Sepet ürünleri için fatura öğelerini oluşturuyoruz
        if cart_items:
            for item in cart_items:
                while True:
                    product_no = "URN" + str(random.randint(1111111, 9999999))
                    if not BilledItems.objects.filter(no=product_no).exists():
                        BilledItems.objects.create(
                            bills=new_billing,
                            product=item.cart_name,
                            no=product_no,
                            price=item.cart_name.product_price,
                            quantity=item.cart_quantity,
                        )
                        break

        # Hızlı satın alım ürünü için fatura öğesini oluşturuyoruz
        if quick_buy:
            while True:
                product_no = "URN" + str(random.randint(1111111, 9999999))
                if not BilledItems.objects.filter(no=product_no).exists():
                    BilledItems.objects.create(
                        bills=new_billing,
                        product=quick_buy.item_name,
                        no=product_no,
                        price=quick_buy.item_name.product_price,
                        quantity=quick_buy.item_quantity,
                    )
                    break

        # Satın alımdan sonra sepeti temizliyoruz.
        CartItem.objects.filter(user=request.user).delete()
        CartItemQuickBuy.objects.filter(user=request.user).delete()

        messages.success(request,"Siparişiniz başarılı bir şekilde alındı!")
        return redirect("/")
    context = {
        "product":product,
        "cart_items":cart_items,
        "quick_buy":quick_buy
      
    }
    return render(request,"intern_app/checkout_quick_buy.html",context)
# Ürünleri görmek için fonksiyon
def product_view(request, category_id=None):
    #Resimler
    resimler = Resimler.objects.all()
    # Oluşturma tarihini göre kaç adet sıralanacağı
    latest_products = Products.objects.order_by('-created_at')[:5]

    # Sayfa görünümü 
    p = Paginator(Products.objects.all(),10)
    page = request.GET.get('page')
    product_page = p.get_page(page)


    products = Products.objects.all()
    category = None
    if category_id:
        category = get_object_or_404(Categories, id=category_id)
        products = Products.objects.filter(product_category=category)
    return render(request, 'intern_app/index.html', {'products': products, 'category': category,"product_page":product_page,"latest_products":latest_products,'resimler':resimler})

# Sepetteki ürünleri güncelleme fonksiyonu


def update_cart(request, item_id):
    if request.method == 'POST':
        # CartItem modelindeki ID'leri alır
        cart_item = CartItem.objects.get(id=item_id)

        # Formdan yeni miktarı alır

        new_quantity = int(request.POST.get(
            'quantity', cart_item.cart_quantity))

        # Sepetteki miktarı günceller ve kaydeder
        cart_item.cart_quantity = new_quantity
        cart_item.save()

    # Güncelledikten sonra bulunduğu sayfaya geri döner
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
# Sepeti görüntüleme fonksiyonu
def cart_view(request):
    # Kullanıcın sepetindeki ürünleri alır
    cart_items = CartItem.objects.filter(user=request.user)
    # Toplam fiyatı alır.
    total_price = sum(item.cart_name.product_price *
                      item.cart_quantity for item in cart_items)

    # AJAX isteği mi kontrol et
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('intern_app/cart_modal.html',
                                {'cart_items': cart_items, 'total_price': total_price}, request)
        return JsonResponse({'html': html})

    return render(request, 'intern_app/cart_modal.html', {'cart_items': cart_items, 'total_price': total_price})



# Sepete ekleme fonksiyonu
def add_to_cart(request, product_id):
    # Products modelinden objeleri ID'lerine göre alır
    product = Products.objects.get(id=product_id)
    if request.method == 'POST':
        # KUllanıcı giriş yapmışmı kontrol et
        if request.user.is_authenticated:

           
            # "Sepete Ekle" butonuna tıklanmışsa, yalnızca sepete ekle
            if request.POST.get('action') == 'add_to_cart':
                # CartItem modelinde objeleri alır
                cart_item, created = CartItem.objects.get_or_create(
                    cart_name=product, user=request.user)
                # name değeri quantity olanları integer türünden alır ve 1 arttırıp kaydeder
                quantity = int(request.POST.get('quantity', 1))
                cart_item.cart_quantity += quantity
                cart_item.save()
                messages.success(request,"Ürününüz sepete başarıyla eklendi!")
                return redirect(request.META.get('HTTP_REFERER'))  # Bulunduğu sayfaya yönlendirir.

            # "Satın Al" butonuna tıklanmışsa, ödeme sayfasına yönlendir
            elif request.POST.get('action') == 'buy_now':
                quick_buy,created = CartItemQuickBuy.objects.get_or_create(user=request.user,item_name=product)
        

                quantity = int(request.POST.get('quantity', 1))
                quick_buy.item_quantity += quantity
                quick_buy.save()
                
                
                
                
                return redirect('intern_app:checkout_quick_buy', product_id=product.id)  # Ödeme sayfasına yönlendir
            # Bulunduğu sayfaya geri döner
            return redirect(request.META.get('HTTP_REFERER'))
        # Giriş yapmadıysa hata mesajı ver 
        messages.warning(request,"Giriş/Kayıt yapmadan sepete ürün ekleyemezsiniz!")
        return redirect(request.META.get('HTTP_REFERER'))
    # Eğer post isteği değilse anasayfaya geri döner.
    return render(request, 'intern_app/index.html', {'product': product})

@csrf_exempt
def clear_quick_buy(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            CartItemQuickBuy.objects.filter(user_id=user_id).delete()

            return JsonResponse({'status':'success'})
        except Exception as e:
            return JsonResponse({'status':'error','message':str(e)})
    return JsonResponse({'status': 'invalid_method'})

@login_required
# Sepetten ürün silme fonksiyonu
def remove_from_cart(request, item_id):
    # Sepetteki ürünü ID'sine göre alır
    cart_item = CartItem.objects.get(id=item_id)
    # Alınan ürünü siler.
    cart_item.delete()

    # Bulunduğu sayfaya geri döner
    return redirect(request.META.get('HTTP_REFERER'))
