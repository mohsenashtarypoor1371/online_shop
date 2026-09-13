from django.views.decorators.cache import never_cache
from .cart import Cart
from . wish import Wish

@never_cache
def show_cart(request):
    return Cart(request).show_cart()

def add_cart(request,pk):
    return Cart(request).add_cart(pk)

def remove(request,pk):
    return Cart(request).remove(pk)

def update(request,pk):
    return Cart(request).update(pk)

def add_wish(request,pk):
    return Wish(request).add_wish(pk)

def delete(request,pk):
    return Wish(request).delete(pk)

@never_cache
def show_wish(request):
    return Wish(request).show_wish()

def order(request):
    return Cart(request).order_()

def order_info(request):
    return Cart(request).order_info()

def payment(request):
    return Cart(request).payment()

def payment_successful(request):
    return Cart(request).payment_success()

def payment_failed(request):
    return Cart(request).payment_failed()