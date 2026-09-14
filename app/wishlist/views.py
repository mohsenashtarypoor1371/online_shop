from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render
from django.template.context_processors import request

from first_app.models import Product,DetailProduct
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from first_app.views import detail_product
from . models import WishList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from . wish import Wish

def wish_list(request):
    wish = Wish(request)
    if request.user.is_authenticated:
        wish1 = WishList.objects.filter(user=request.user)
        return render(request,'wishlist/wish.html',{'wish1':wish1,'wish':wish})
    else:
        wish1= WishList.objects.none()
        return  render(request,'wishlist/wish.html',{'wish1':wish1,'wish':wish})


def add_wish(request,pk):
    Wish(request).add_wish(pk)
    return redirect('wishlist:wish_list')

def remove(request,pk):
    Wish(request).remove(pk)
    return redirect('wishlist:wish_list')

