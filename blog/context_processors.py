
from .models import Cart

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        
        cart_items = Cart.objects.filter(user=request.user)
        count = cart_items.count() 
    return {'cart_count': count}