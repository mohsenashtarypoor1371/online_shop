from . cart import Cart
from django.shortcuts import get_object_or_404
from first_app.models import Product
from django.shortcuts import render

def cart(request):
    return {'cart':Cart(request)}
def pro(request):
    return {'product':Product(request)}