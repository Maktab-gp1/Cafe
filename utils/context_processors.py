from cart.cart import Cart
from shop.models import Cafe
def cart(request):
    return {'cart': Cart(request)}

def cafe_info(request):
    cafe_info = Cafe.objects.first()
    return {'cafe_info' : cafe_info}