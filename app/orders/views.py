from .order import Ordered
from django.shortcuts import render,redirect
from .models import Order,OrderItem
from django.views.decorators.cache import never_cache
from .form import *

# Create your views here.


def show_order(request,pk):
    order = Order.objects.get(id=pk)
    item = OrderItem.objects.filter(order=order)
    return render(request,'order/order.html',{'order':order,'item':item})

def order(request):
    return  Ordered(request).orders()

def order_item(request,order):
    return Ordered(request).order_items(order)

def final_order(request):
    return Ordered(request).final_order()

def my_order(request):
    return Ordered(request).my_order()

def remove(request,pk):
    return Ordered(request).remove(pk)

def payment(request):
    return Ordered(request).payment()

def product_paid(request):
    return Ordered(request).product_paid()

def detail_paid(request,pk):
    return Ordered(request).detail_paid(pk)