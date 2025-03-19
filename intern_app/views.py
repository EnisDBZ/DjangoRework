from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout,get_user_model,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Products , CartItem , Categories 
from django.template.loader import render_to_string
from django.http import JsonResponse



# Create your views here.
def categories_list(request):
    categories = Categories.get_main_categories() # Tüm kategorileri al
   

    context = {
        'categories':categories,
     
       
    }
    return render(request, "intern_app/categories.html",context)

def categories(request, slug):
    category = get_object_or_404(Categories,slug=slug)
    products = Products.objects.filter(product_category=category)
    sub_categories = category.sub_categories.all()
    context = {
        'category':category,
        'products' : products,
        'sub_categories': sub_categories
    }

    return render(request, "intern_app/categories_added.html", context)


"""def subcategory(request):
    sub_category = SubCategories.objects.all()
    context ={
        'sub_category' : sub_category
    }
    return render(request,'intern_app/sub_categories.html',context)"""

def search_view(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        posts = Products.objects.filter(product_name__icontains = search_query)
        return render(request,'intern_app/search_result.html',{'query':search_query,'posts':posts})
    else:
        return render(request,'intern_app/search_result.html',{})


def index(request):
    return render(request,'intern_app/index.html')

@login_required
def setting(request):
    return render(request,'intern_app/setting.html')

# Authentication #
User = get_user_model()

def update_names(request):
    if request.method == 'POST':
        isim = request.POST.get('isim')
        soyisim = request.POST.get('soyisim')

        if len(isim) < 2:
            messages.error(request,'İsminiz en az 2 karakterli olabilir!')
            return redirect('intern_app:update_names')
        if len(soyisim) < 2:
            messages.error(request,'Soyisminiz en az 2 karakterli olabilir!')
            return redirect('intern_app:update_names')
        
        request.user.first_name = isim
        request.user.last_name = soyisim
        request.user.save()

        update_session_auth_hash(request,request.user) #Kullanıcı çıkış yapmasın
        messages.success(request,'Bilgileriniz başarıyla güncellendi!')
        return redirect('intern_app:settings')
    return render(request,'intern_app/setting.html')


def update_email(request):
    if request.method == 'POST':
        old_email = request.POST.get('old_email')
        new_email = request.POST.get('new_email')

        if request.user.email != old_email:
            messages.error(request,'Eski e-posta adresinizi yanlış girdiniz!')
            return redirect('intern_app:update_email')
        
        #Değiştirilmek istenen e-posta kullanımda mı ?
        if User.objects.filter(email = new_email).exists():
            messages.error(request,'Bu eposta adresi zaten kullanılmakta!')
            return redirect('intern_app:update_email')
        
        request.user.email = new_email
        request.user.save()

        update_session_auth_hash(request,request.user)
        messages.success(request,'E-posta adresiniz başarıyla güncellendi!')
        return redirect('intern_app:settings')
    return render(request,'intern_app/setting.html')
def update_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        if not request.user.check_password(old_password):
            messages.error(request,'Eski şifrenizi yanlış girdiniz!')
            return redirect('intern_app:update_password')
        
        if len(new_password) < 8:
            messages.error(request,'Yeni şifreniz en az 8 karakter olmak zorunda!')
            return redirect("intern_app:update_password")
        
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request,request.user) # Oturumu açık tutmak için

        messages.success(request,'Şifreniz başarıyla güncellendi!')
        return redirect('intern_app:settings')
    
    return render(request,"intern_app/setting.html")

def redirect_url_(request):
    if request.user.is_authenticated :
        redirect_url = 'index'
    else:
        redirect_url = 'login'

    return render(request,'intern_app/index.html',{'redirect_url':redirect_url})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password = password)

        if user is not None:
            login(request,user)
            if user.is_staff or user.is_superuser:
                login(request,user)
                return redirect('/admin/')
            elif user.is_authenticated:
                return redirect('intern_app:index')
            
            return render(request,'intern_app/index.html')
        else:
            return render(request,'registration/login.html',{'error':'Geçersiz giriş.'})
        
    return render(request,'registration/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('intern_app:index')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # Check the password if they are matching or not

        if password != confirm_password:
            messages.error(request,'Şifreler eşleşmiyor.')
            return render(request,'registration/signup.html')
        # Create the user 

        try:
            user = User.objects.create_user(email = email,username = username,password = password)
            user.save()
            messages.success(request,'Başarıyla kayıt oldunuz. Giriş yapabilirsiniz.')
            return redirect('intern_app:login')
        except Exception as e:
            messages.error(request,'Kayıt olurken bir hata meydana geldi:' + str(e))

    return render(request, 'registration/signup.html')

    


# Authentication #

# Shopping #

def product_view(request,category_id = None):
    products = Products.objects.all()
    category = None
    if category_id:
        category = get_object_or_404(Categories,id = category_id)
        products = Products.objects.filter(product_category=category)
    return render(request,'intern_app/index.html',{'products':products, 'category':category})


def update_cart(request, item_id):
    if request.method == 'POST':
        # Get the CartItem object by its ID
        cart_item = CartItem.objects.get(id=item_id)

        # Get the new quantity from the form
        new_quantity = int(request.POST.get('quantity', cart_item.cart_quantity))  # Default to current quantity if not provided

        # Update the cart item's quantity and save
        cart_item.cart_quantity = new_quantity
        cart_item.save()

    # After updating, redirect the user back to the cart page
    return redirect('intern_app:cart')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.cart_name.product_price * item.cart_quantity for item in cart_items)

    # AJAX isteği mi kontrol et
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('intern_app/cart_modal.html', {'cart_items': cart_items, 'total_price': total_price}, request)
        return JsonResponse({'html': html})

    return render(request, 'intern_app/cart_modal.html', {'cart_items': cart_items, 'total_price': total_price})
@login_required
def add_to_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    if request.method == 'POST':
        cart_item, created = CartItem.objects.get_or_create(cart_name = product,user = request.user)
        quantity = int(request.POST.get('quantity',1))
        cart_item.cart_quantity += quantity
        cart_item.save()
        return redirect('intern_app:index')

    # If it's not a POST request, render the product page with the form
    return render(request, 'intern_app/index.html', {'product': product})
@login_required
def remove_from_cart(request,item_id):
    # Get the cart item based on the item_id
    cart_item = CartItem.objects.get(id=item_id)

    cart_item.delete()

        

    # Redirect to the cart page after updating
    return redirect('intern_app:cart')
