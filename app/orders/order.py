from itertools import product

from . form import OrderForm
from django.shortcuts import redirect,render
from .models import Order,OrderItem
from cart.models import CartList
from cart.cart import Cart
from django.contrib import messages
from django.shortcuts import get_object_or_404



class Ordered:
    def __init__(self,request):
        self.request = request
        self.user = request.user
        self.session = request.session



    def orders(self):
        if self.cart_is_empty():
            return redirect('cart:show_cart')
        if self.request.method == 'GET':
            if self.user.is_authenticated:
                last_order = Order.objects.filter(user=self.user).last()
                if last_order:
                    form = OrderForm(initial={'name':last_order.name,'phone':last_order.phone,
                                          'address':last_order.address})
                else:
                    form = OrderForm()
                return render(self.request, 'form/order.html', {'form': form})
            else:
                last_order = Order.objects.filter(
                    session_key=self.request.session.session_key).last()
                if last_order:
                    form = OrderForm(initial={'name':last_order.name,
                                              'phone':last_order.phone,
                                              'address':last_order.address})
                else:
                    form = OrderForm()
                return render(self.request, 'form/order.html', {'form': form})
        if self.request.method == 'POST':
            form = OrderForm(self.request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                name = cd['name']
                phone = cd['phone']
                address = cd['address']
                if not self.request.session.session_key:
                    self.request.session.create()
                order = Order.objects.create(user=self.user if self.user.is_authenticated
            else None
                ,name=name,phone=phone,address=address,
                                             session_key=self.request.session.session_key)
                self.order_items(order)
                messages.success(self.request,'Your order has been successfully placed.')
                return render(self.request,'order/success.html')
            return render(self.request,'form/order.html',{'form':form})

    def order_items(self,order):
        if self.user.is_authenticated:
            cart = CartList.objects.filter(user=self.user)
            for i in cart:
                 OrderItem.objects.create(order=order,
                                         product=i.product,quantity=i.quantity,price=i.price)
            cart.delete()

        else:
            cart1 = Cart(self.request)
            for j in cart1:
                OrderItem.objects.create(order=order,quantity=j['quantity'],
                                         product=j['product'],price=j['price'])
            cart1.clear()


    def my_order(self):
        if self.user.is_authenticated:
            order_it = OrderItem.objects.filter(order__user=self.user,order__status='draft')
            return render(self.request, 'order/my_order.html',
                          {'order_it': order_it})
        else:
            order_it = OrderItem.objects.filter(order__session_key=self.request.session.session_key,
                                                order__status='draft')
            return render(self.request,'order/my_order.html',
                            {'order_it':order_it})

    def remove(self,pk):
        order_item=OrderItem.objects.get(id=pk)
        ord1 = order_item.order
        order_item.delete()
        if not OrderItem.objects.filter(order=ord1).exists():
            ord1.delete()
        return redirect('orders:my_order')


    def cart_is_empty(self):
        if self.user.is_authenticated:
            if not CartList.objects.filter(user=self.user).exists():
                return redirect('cart:show_cart')
        else:
            cart = Cart(self.request)
            if not cart.cart:
                return redirect('cart:show_cart')


    def final_order(self):
        if self.user.is_authenticated:
            order = Order.objects.filter(user=self.user,status='draft')
            order.update(status='pending')
            order1 = OrderItem.objects.filter(order__user=self.user,order__status='pending')
            return render(self.request,'order/final-order.html',{'order1':order1})
        else:
            order = Order.objects.filter(session_key=self.request.session.session_key,status='draft')
            order.update(status='pending')
            order1 = OrderItem.objects.filter(order__session_key=self.request.session.session_key,
                                              order__status='pending')
            return render(self.request, 'order/final-order.html',
                          {'order1': order1})


    def payment(self):
        if self.request.method == 'POST':
            if self.user.is_authenticated:
                result = self.request.POST.get('result')
                if result == 'success':
                        order = Order.objects.filter(user=self.user,status='pending')
                        order1 = OrderItem.objects.filter(order__user=self.user,order__status='pending')
                        for i in order1:
                            if i.product.stock >= i.quantity:
                                i.product.stock -= i.quantity
                                i.product.save()
                            else:
                                messages.error(self.request,'out of stock')
                        order.update(status='paid')
                        order1 = OrderItem.objects.filter(order__user=self.user,order__status='paid')
                        messages.success(self.request,'pay successful')
                        return render(self.request, 'order/payment.html', {'order1': order1})
                else:
                    order1 = OrderItem.objects.filter(order__user=self.user,order__status='pending')
                    messages.error(self.request,'pay field')

                    return render(self.request, 'order/payment.html', {'order1': order1})
            else:
                result = self.request.POST.get('result')
                if result == 'success':
                        order = Order.objects.filter(session_key=self.request.session.session_key,status='pending')
                        order.update(status='paid')
                        order1 = OrderItem.objects.filter(order__session_key=self.request.session.session_key,order__status='paid')
                        messages.success(self.request,'pay successful')
                        return render(self.request, 'order/payment.html', {'order1': order1})
                else:
                    order1 = OrderItem.objects.filter(order__session_key=self.request.session.session_key,order__status='pending')
                    messages.error(self.request, 'pay field')
                    return render(self.request,'order/payment.html',{'order1':order1})
        else:
            order1 = OrderItem.objects.filter(order__user=self.user, order__status='pending')

            return render(self.request, 'order/payment.html', {'order1': order1})


    def product_paid(self):
        if self.user.is_authenticated:
            order1 = OrderItem.objects.filter(order__user=self.user,order__status='paid')
            total =0
            for i in order1:
                f = i.price * i.quantity
                total += f
        else:
            order1 = OrderItem.objects.filter(order__session_key=self.request.session.session_key,
                                              order__status='paid')
            total = 0
            for i in order1:
                f = i.price *i.quantity
                total += f
        return render(self.request, 'order/product_paid.html', {'order1': order1,'total':total})



    def detail_paid(self,pk):
        if self.request.method == 'GET':
            if self.user.is_authenticated:
                order = get_object_or_404(Order,id=pk)
                order1 = OrderItem.objects.filter(order=order,order__user=self.user,order__status='paid')
            else:
                order = get_object_or_404(Order, id=pk)
                order1 = OrderItem.objects.filter(order=order,order__session_key=self.request.session.session_key
                                                 ,order__status='paid')
            return render(self.request,'order/detail_paid.html',{'order1':order1})
        return render(self.request,'order/product_paid.html')














