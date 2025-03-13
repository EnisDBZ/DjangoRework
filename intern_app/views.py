from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Products , CartItem
from django.template.loader import render_to_string
from django.http import JsonResponse

# Create your views here.
def search_view(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        posts = Products.objects.filter(product_name__icontains = search_query)
        return render(request,'intern_app/search_result.html',{'query':search_query,'posts':posts})
    else:
        return render(request,'intern_app/search_result.html',{})


def index(request):
    return render(request,'intern_app/index.html')

# Authentication #
User = get_user_model()

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

def product_view(request):
    products = Products.objects.all()
    return render(request,'intern_app/index.html',{'products':products})

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
