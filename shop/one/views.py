from django.shortcuts import render
from .shop import Shop

# Create your views here.
def shop_show(request):
    return Shop(request).shop_show()

def detail_pro(request,slug):
    return Shop(request).detail_pro(slug)

def search(request):
    return Shop(request).search()

def contact(request):
    return Shop(request).contact()

def login(request):
    return Shop(request).login()

def sign_up(request):
    return Shop(request).sign_up()

def log_out(request):
    return Shop(request).log_out()

def recruitment(request):
    return Shop(request).recruitment()

def comment_product(request,slug):
    return Shop(request).comment(slug)

def delete_comment(request,pk):
    return Shop(request).delete_comment(pk)

def edit_comment(request,pk):
    return Shop(request).edit_comment(pk)