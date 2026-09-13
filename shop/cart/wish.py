from django.shortcuts import get_object_or_404, render
from one.models import Product
from django.shortcuts import redirect
class Wish:
    def __init__(self,request):
        self.request=request
        self.session = request.session
        wish = self.session.get('wish')
        if not wish:
            wish = self.session['wish'] = {}
        self.wish = wish

    def save(self):
        self.session.modified=True

    def add_wish(self,pk):
        product = get_object_or_404(Product,id=pk)
        product_id = str(product.id)
        if product_id not in self.session['wish']:
            self.session['wish'][product_id] = True
        self.session.modified=True
        return redirect('cart:show_wish')

    def show_wish(self):
        wish = self.session['wish']
        list=[]
        for i in wish.keys():
            p = int(i)
            product = Product.objects.get(id=p)
            list.append(product)
        return render(self.request, 'one_temp/content/favorite.html',{'list':list})


    def delete(self,pk):
        product = get_object_or_404(Product,id=pk)
        product_id = str(product.id)
        if product_id in self.session['wish']:
            del self.session['wish'][product_id]
        self.session.modified=True
        return redirect('cart:show_wish' )

