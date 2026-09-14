from traceback import print_tb

from .models import WishList
from django.shortcuts import get_object_or_404
from first_app.models import Product

class Wish:
    def __init__(self,request):
        self.request = request
        self.user = request.user
        self.session = request.session
        wish = self.session.get('wish')
        if not wish:
            wish = self.session['wish']={}
        self.wish= wish

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_id = self.wish.keys()
        products = Product.objects.filter(id__in=product_id)
        for i in products:
            yield i

    def remove(self,pk):
        if self.user.is_authenticated:
            WishList.objects.filter(id=pk,user=self.user).delete()
        product_id = str(pk)
        if product_id in self.wish:
           del self.wish[product_id]
        self.save()


    def add_wish(self,pk):
        if self.user.is_authenticated:
            product = get_object_or_404(Product,id=pk)
            wish1 = WishList.objects.get_or_create(product=product,user=self.user)
            return wish1
        else:
            product_id = str(pk)
            if product_id not in self.wish:
                self.wish[product_id]={}
            self.save()











