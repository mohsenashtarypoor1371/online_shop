from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from first_app. models import Product
from .cart import Cart
from django.shortcuts import redirect

# Create your views here.
@never_cache
def show_cart(request):
    cart = Cart(request)
    return render(request,'cart/html/cart.html',{'cart':cart,
                                                 'total_price':cart.total_price()})
def add_cart(request,pk):
    product1 = get_object_or_404(Product,id=pk)
    cart = Cart(request)
    cart.add(product1)
    return redirect('cart:show_cart')


def delete_cart(request,pk):
    cart = Cart(request)
    products= get_object_or_404(Product,id=pk)
    cart.remove(products)
    return redirect('cart:show_cart')

def update_cart(request,pk):
    cart = Cart(request)
    product = get_object_or_404(Product,id=pk)
    quantity =(request.POST.get('quantity'))
    if not quantity:
        messages.error(request, 'enter value')
        return redirect('cart:show_cart')
    else:
        quantity = int(quantity)
        cart.update(product,quantity)
        return redirect('cart:show_cart')


def total_price(request):
    Cart(request).total_price()
    return render(request,'cart/html/cart.html')

from django.http import HttpResponse
def total_quantity(request):
    Cart(request).total_quantity()
    return render(request,'cart/html/cart.html')

def total_price_all(request):
    Cart(request).total_price_all()
    return render(request,'cart/html/cart.htm')

def login_cart(request):
    Cart(request).login_cart()
    return render(request, 'cart/html/cart.htm')