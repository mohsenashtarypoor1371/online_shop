from email.policy import default
from itertools import product

from django.contrib import messages

from first_app.models import Product
from django.shortcuts import get_object_or_404
from . models import CartList
from django.shortcuts import redirect



class Cart:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        self.user = request.user
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart']={}
        self.cart = cart

    def clear(self):
        if 'cart' in self.session:
            del self.session['cart']
            self.session.modified=True

    def get_item(self):
        if self.user.is_authenticated:
            return CartList.objects.filter(user=self.user)
        return self

    def add(self,product,quantity=1):
        if self.user.is_authenticated:
            cart,created = CartList.objects.get_or_create(user=self.user,product=product,
                                                          defaults={'quantity':quantity,
                                                                    'price':product.price})
            if not created:
                cart.quantity += quantity
                cart.save()
            return
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]={'quantity':0,'price':product.price}
        self.cart[product_id]['quantity'] += int(quantity)
        self.save()

    def save(self):
        self.session.modified= True

    def __iter__(self):
        if self.user.is_authenticated:
            carts = CartList.objects.filter(user=self.user)
            for i in carts:
                yield {'product':i.product,'quantity':i.quantity}
        else:
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            cart = self.cart.copy()
            for pro in products:
                cart[str(pro.id)]['product']=pro
            for item in cart.values():
                yield item

    def remove(self,product):
        if self.user.is_authenticated:
            cart = CartList.objects.filter(user=self.user,product=product)
            cart.delete()
            return
        product_id =str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self,product,quantity):
        if self.user.is_authenticated:
            cart = CartList.objects.get(product=product,user=self.user)
            if quantity > 0:
                cart.quantity = quantity
                cart.save()
            else:
                cart.delete()
            return
        product_ids = str(product.id)
        if product_ids in self.cart and quantity > 0:
            self.cart[product_ids]['quantity']= quantity
            self.save()
        else:
            self.remove(product)

    def total_price(self):
        total = 0
        for time in self:
            g= int(time['quantity'])
            h = time['product'].price
            total += g*h
        return total

    def total_quantity(self):
        if self.user.is_authenticated:
            total = 0
            cart = CartList.objects.filter(user=self.user)
            for i in cart:
                total += i.quantity
            return total
        total =0
        for i in self.cart.values():
             t=(i['quantity'])
             total +=t
        return (total)

    def total_price_all(self):
        total = 0
        for i in self:
            pro = i['product'].price*int(i['quantity'])
            total += pro
        return (total)


    def login_cart(self):
        for i,j in self.cart.items():
            product = Product.objects.get(id=i)
            if self.user.is_authenticated:
                cart = CartList.objects.update_or_create(user=self.user,product=product,
                                                defaults={'quantity':j['quantity']})


