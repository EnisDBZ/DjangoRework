from .models import CartItem

def cart_items_processor(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.cart_name.product_price * item.cart_quantity for item in cart_items)
    else:
        cart_items = []
        total_price = 0

    return {'cart_items': cart_items, 'total_price': total_price}
