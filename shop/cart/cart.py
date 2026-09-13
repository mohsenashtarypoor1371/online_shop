from itertools import product

from django.contrib import messages
from django.shortcuts import redirect,render
from django.shortcuts import get_object_or_404
from .form import *
from .models import *



class Cart:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart']={}
        self.cart = cart

    def show_cart(self):
        total = self.total_price()
        product = self.session['cart'].keys()

        product1 = Product.objects.filter(id__in=product)
        cart = self.session['cart']
        item = []
        for i in product1:
            p=str(i.id)
            quantity = cart[p]
            item.append({'quantity':quantity,'product':i})
        return render(self.request,'cart_temp/content/show_cart.html',
                      {'item':item,'total':total})


    def add_cart(self,pk):
        cart = self.request.session['cart']
        product = get_object_or_404(Product,id=pk)
        product_id = str(product.id)
        if product.stock <= 0:
            messages.error(self.request,'out of stock')
            return redirect('cart:show_cart')
        if product_id not in cart:
            cart[product_id] = 1
        else:
            if cart[product_id]<product.stock:
                cart[product_id] += 1
            else:
                messages.error(self.request, 'out of stock')
                return redirect('cart:show_cart')
        self.request.session.modified=True
        return redirect('cart:show_cart')


    def total_price(self):
        total = 0
        cart = self.session['cart']
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            total += product.price*quantity
        return total

    def remove(self,pk):
        if self.request.method == 'POST':
            product_id = str(pk)
            if product_id in self.session['cart']:
                del self.session['cart'][product_id]
            self.session.modified = True
            return redirect('cart:show_cart')
        else:
            return render(self.request,'cart_temp/content/show_cart.html')


    def update(self,pk):
        product = get_object_or_404(Product,id=pk)
        product_id = str(product.id)
        query = self.request.POST.get('query')
        if query and int(query) != 0 and int(query)<=product.stock:
            self.session['cart'][product_id]=int(query)
        else:
            messages.error(self.request, 'The selected number exceeds the available stock.')
        self.session.modified=True
        return redirect('cart:show_cart')


    def order_(self):
        if self.request.user.is_authenticated:
            if self.request.method == 'POST':
                form = OrderForm(self.request.POST)
                if form.is_valid():
                    cart = self.session.get('cart',{})
                    if not cart:
                        return redirect('cart:show_cart')
                    cd = form.cleaned_data
                    name = cd['name']
                    phone = cd['phone']
                    address = cd['address']
                    self.request.session['guest']={'name':cd['name'],
                                                                     'phone':cd['phone'],'address':cd['address']}
                    cart = self.request.session['cart']
                    for c, d in cart.items():
                        product = Product.objects.get(id=c)
                        if d > product.stock:
                            return redirect('cart:show_cart')
                    order = Order.objects.filter(user=self.request.user,status='pending').first()
                    if not order:
                        order = Order.objects.create(user=self.request.user,name=name,phone=phone,address=address)
                        cart = self.session['cart']
                        for pro_id,qo in cart.items():
                            product= Product.objects.get(id=pro_id)
                            order_item = OrderItem.objects.create(order=order,product=product,
                                                          quantity=qo,price=product.price)
                    else:
                        cart = self.request.session['cart']
                        for item,quantity in cart.items():
                            product = Product.objects.get(id=item)
                            order_item = OrderItem.objects.create(order=order,product=product,quantity=quantity,
                                                                  price=product.price)
                    self.session['cart'] ={}
                    self.session.modified=True
                    return redirect('cart:order_info')
                return render(self.request, 'cart_temp/content/checkout.html',{'form':form})
            guest = self.request.session.get('guest',{})
            form = OrderForm(initial=guest)
            return render(self.request,'cart_temp/content/checkout.html',{'form':form})
        else:
            if self.request.method =='POST':
                form = OrderForm(self.request.POST)
                if form.is_valid():
                    cart= self.request.session.get('cart',{})
                    if not cart:
                        return redirect('cart:show_cart')
                    cd = form.cleaned_data
                    name = cd['name']
                    phone = cd['phone']
                    address = cd['address']
                    self.request.session['guest'] = {'name': cd['name'],
                                                     'phone': cd['phone'],
                                                     'address': cd['address']}
                    cart = self.request.session['cart']
                    for c,d in cart.items():
                        product = Product.objects.get(id=c)
                        if d > product.stock:
                            return redirect('cart:show_cart')
                    order = Order.objects.create(user=None,name=name,phone=phone,address=address)
                    self.request.session['order_id']=order.id
                    guest_info = self.request.session.get('guest_info', [])
                    guest_info.append(order.id)
                    self.request.session['guest_info']=guest_info
                    cart = self.session['cart']
                    for g,p in cart.items():
                        product = Product.objects.get(id=g)
                        order_item = OrderItem.objects.create(
                            order=order,product=product,quantity=p,price=product.price)
                    self.session['cart']={}
                    self.session.modified=True
                    return redirect('cart:order_info')
                return render(self.request, 'cart_temp/content/checkout.html', {'form': form})
            guest1 = self.request.session.get('guest',{})
            form = OrderForm(guest1)
            return render(self.request, 'cart_temp/content/checkout.html', {'form': form})

    def order_info(self):
        total = self.total_number_of_purchased_item()
        total_number = self.total_product_price_cart()
        if self.request.user.is_authenticated:
            user = self.request.user
            orders = Order.objects.filter(user=user)
            item = OrderItem.objects.filter(order__user=user)
            p = ''
            for items in orders:
                a = items.status
                p = a
            return render(self.request,'cart_temp/content/order_info.html',
                        {'orders':orders,'user':user,'item':item,'total':total,'total_number':total_number,
                         'p':p
                       })
        else:
            guest_info= self.request.session.get('guest_info')
            if guest_info:
                order1 = Order.objects.filter(id__in=guest_info)
                order_item=OrderItem.objects.filter(order__id__in=guest_info)
                p=''
                for i in order1:
                    a= i.status
                    p = a
                return render(self.request,'cart_temp/content/order_info.html',
                          {'order1':order1,'order_item':order_item,'total':total,
                           'total_number':total_number,'p':p
                           })
            else:
                return redirect('one:shop_show')

    def total_product_price_cart(self):
        if self.request.user.is_authenticated:
            order_item = OrderItem.objects.filter(order__user=self.request.user)
            num = 0
            for j in order_item:
                p = j.price * j.quantity
                num += p
            return num
        else:
            num = 0
            cart = self.request.session.get('guest_info',[])
            item = OrderItem.objects.filter(order__id__in=cart)
            if item.exists():
                for i in item:
                    p=i.price * i.quantity
                    num += p
                return num
            else:
                return 0



    def total_number_of_purchased_item(self):
        if self.request.user.is_authenticated:
            order_item = OrderItem.objects.filter(order__user=self.request.user)
            num = 0
            for i in order_item:
                a = i.quantity
                num += a
            return num
        else:
            cart = self.request.session.get('guest_info',[])
            order_item = OrderItem.objects.filter(order__id__in=cart)
            if order_item.exists():
                num1 = 0
                for i in order_item:
                    p =i.quantity
                    num1 += p
                return num1
            else:
                return 0

    def payment(self):
        if self.request.user.is_authenticated:
            order = Order.objects.filter(user=self.request.user,status__in=['pending','processing']).first()
            if order:
                order.status = 'processing'
                order.save()
            order_item2 = OrderItem.objects.filter(order=order)
            return render(self.request, 'cart_temp/content/payment.html',
                          {'order_item2':order_item2})

        else:
            cart = self.request.session.get('order_id')
            order = Order.objects.get(id=cart)
            order_item=OrderItem.objects.filter(order=order)
        return render(self.request,'cart_temp/content/payment.html',
                      {'order_item':order_item})

    def payment_success(self):
        if self.request.user.is_authenticated:
            order = Order.objects.filter(user=self.request.user,status='processing').first()
            if order:
                order_item2 = OrderItem.objects.filter(order=order)
                messages.success(self.request,'pay success')
                order.status ='paid'
                order.save()
                for item in order_item2:
                    product=item.product
                    product.stock -= item.quantity
                    product.save()
                return render(self.request, 'cart_temp/content/payment_successful.html',
                          {'order_item2': order_item2})
            else:
                return redirect('cart:order_info')
        else:
            cart = self.request.session.get('guest_info')
            order = Order.objects.filter(id__in=cart)
            order_item = OrderItem.objects.filter(order__in=order)
            for i in order:
                i.status = 'paid'
                i.save()
            for item in order_item:
                if item.product.stock < item.quantity:
                    messages.error(self.request,'stock is lower quantity')
                    return redirect('cart:order_info')
                product=item.product
                product.stock -= item.quantity
                product.save()
        return render(self.request, 'cart_temp/content/payment_successful.html',
                      {'order_item': order_item})


    def payment_failed(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            order = Order.objects.filter(user=user,status='processing').first()
            if order:
                order_item2 = OrderItem.objects.filter(order=order)
                order.status='pending'
                order.save()
                return render(self.request, 'cart_temp/content/payment_failed.html',
                              {'order_item2': order_item2})
            else:
                messages.error(self.request,'The payment failed.')
                return redirect('cart:order_info')
        else:
            cart = self.request.session.get('order_id')
            order_item = OrderItem.objects.filter(order__id=cart)
            order = Order.objects.get(id=cart)
            order.status='pending'
            order.save()
        return render(self.request, 'cart_temp/content/payment_failed.html', {'order_item': order_item})
