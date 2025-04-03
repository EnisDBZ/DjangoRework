from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Products, CartItem, Categories
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import admin


# Create your views here.

# Kendi admin panelim #

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
        'sub_categories': sub_categories
    }

    return render(request, "intern_app/categories_added.html", context)


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
                return redirect('/admin/')
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

# Ürünleri görmek için fonksiyon
def product_view(request, category_id=None):
    products = Products.objects.all()
    category = None
    if category_id:
        category = get_object_or_404(Categories, id=category_id)
        products = Products.objects.filter(product_category=category)
    return render(request, 'intern_app/index.html', {'products': products, 'category': category})

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


@login_required
# Sepete ekleme fonksiyonu
def add_to_cart(request, product_id):
    # Products modelinden objeleri ID'lerine göre alır
    product = Products.objects.get(id=product_id)
    if request.method == 'POST':
        # CartItem modelinde objeleri alır
        cart_item, created = CartItem.objects.get_or_create(
            cart_name=product, user=request.user)
        # name değeri quantity olanları integer türünden alır ve 1 arttırıp kaydeder
        quantity = int(request.POST.get('quantity', 1))
        cart_item.cart_quantity += quantity
        cart_item.save()
        # Bulunduğu sayfaya geri döner
        return redirect(request.META.get('HTTP_REFERER'))

    # Eğer post isteği değilse anasayfaya geri döner.
    return render(request, 'intern_app/index.html', {'product': product})


@login_required
# Sepetten ürün silme fonksiyonu
def remove_from_cart(request, item_id):
    # Sepetteki ürünü ID'sine göre alır
    cart_item = CartItem.objects.get(id=item_id)
    # Alınan ürünü siler.
    cart_item.delete()

    # Bulunduğu sayfaya geri döner
    return redirect(request.META.get('HTTP_REFERER'))
