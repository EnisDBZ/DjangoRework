from .models import CartItem , Categories
from django.shortcuts import get_object_or_404

def cart_items_processor(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.cart_name.product_price * item.cart_quantity for item in cart_items)
    else:
        cart_items = []
        total_price = 0

    return {'cart_items': cart_items, 'total_price': total_price}

def categories_processor(request):
    categories = Categories.get_main_categories()  # Kendi metodunla al
    return {'categories': categories}  # Template'e gönder

def sub_categories_processor(request):
    if 'slug' in request.resolver_match.kwargs:
        slug = request.resolver_match.kwargs.get('slug')
        category = get_object_or_404(Categories,slug=slug)
        sub_categories = category.sub_categories.all()
        return {'sub_categories':sub_categories}
    return {'sub_categories':[]}