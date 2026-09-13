from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
from . models import Product,Contact,CommentProduct
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchRank,SearchQuery,SearchVector
from  django.shortcuts import redirect
from django.db.models import Q
from .form import *
from django.contrib.auth import login,logout,authenticate


class Shop:
    def __init__(self,request):
        self.request = request
        self.user = User

    def save(self):
        self.request.modified = True

    def shop_show(self):
        product = Product.objects.all()
        p = Paginator(product,1)
        page_number = self.request.GET.get('page')
        try:
            page = p.get_page(page_number)
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(p.num_pages)
        return render(self.request,'one_temp/content/show.html',{'page':page})

    def detail_pro(self,slug):
            product = get_object_or_404(Product,slug=slug)
            comment = CommentProduct.objects.filter(product=product)
            return render(self.request,'one_temp/content/detail.html',
                          {'product':product,'comment':comment})


    def search(self):
        if self.request.method == 'GET':
            query = self.request.GET.get('q')
            if query:
                search =  Product.objects.filter(Q(name_product__icontains=query))
                return render(self.request,'one_temp/content/search.html',{'search':search})
            else:
                return redirect('one:shop_show')
        else:
            return redirect('one:shop_show')

    def contact(self):
        if self.request.method == 'POST':
            form = ContactForm(self.request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                f_name =cd['f_name']
                l_name = cd['l_name']
                email = cd['email']
                subject = cd['subject']
                message =cd['message']
                contact = Contact.objects.create(f_name=f_name,l_name=l_name,email=email,
                                                 subject=subject,message=message)
                contact.save()
                return redirect('one:shop_show')
            else:
                return redirect('one:contact')
        else:
            form = ContactForm()
            return render(self.request, 'one_temp/content/contact.html', {'form': form})

    def login(self):
        if self.request.method == 'POST':
            form = LoginForm(self.request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                username=cd['username']
                password=cd['password']
                user = authenticate(username=username,password=password)
                if user is not None:
                    if user.is_active:
                        login(self.request,user)
                        return redirect('one:shop_show')
                    else:
                        messages.error(self.request, 'user is unactive')
                        return render(self.request,'one_temp/content/login.html')
                else:
                    messages.error(self.request,'user is None')
                    return render(self.request, 'one_temp/content/login.html')
            else:
                form = LoginForm()
                messages.error(self.request,'please enter the value')
                return render(self.request, 'one_temp/content/login.html', {'form': form})

        else:
            form = LoginForm()
            return render(self.request,'one_temp/content/login.html',{'form':form})

    def sign_up(self):
        if self.request.method == 'POST':
            form = SignUpForm(self.request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                first_name =cd['first_name']
                last_name = cd['last_name']
                username = cd['username']
                password = cd['password']
                email = cd['email']
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email)
                login(self.request,user)
                return redirect('one:shop_show')
            else:
                messages.error(self.request,'form is invalid')
                return render(self.request, 'one_temp/content/sign_up.html', {'form': form})
        else:
            form = SignUpForm()
            return render(self.request, 'one_temp/content/sign_up.html',{'form':form})

    def log_out(self):
       logout(self.request)
       return redirect('one:shop_show')

    def recruitment(self):
        if self.request.method == 'POST':
            form = RecruitmentForm(self.request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                f_name = cd['f_name']
                l_name = cd['l_name']
                email = cd['email']
                address = cd['address']
                phone = cd['phone']
                job_title = cd['job_title']
                skill = cd['skill']
                work_history = cd['work_history']
                message = send_mail('recruitment',f'{f_name}{l_name}{email}{address}{phone}{job_title}'
                                                  f'{skill}{work_history}','mohsenashtrypoor@gmail.com',['mohsenashtrypoor@gmail.com'],
                                fail_silently=False)
                return redirect('one:shop_show')
            else:
                return render(self.request, 'one_temp/content/recruit.html', {'form': form})

        else:
            form =RecruitmentForm()
            return render(self.request,'one_temp/content/recruit.html',{'form':form})



    def comment(self,slug):
        if not self.request.user.is_authenticated:
            return redirect('one:login')
        product = get_object_or_404(Product,slug=slug)
        if self.request.method == 'POST':
            form = CommentForm(self.request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                text = cd['text']
                rating = cd['rating']
                if self.request.user.is_authenticated:
                    comment = CommentProduct.objects.create(user=self.request.user,product=product,text=text,rating=rating)
                    return redirect('one:detail',product.slug)
                else:
                    comment = CommentProduct.objects.create(product=product, text=text,
                                                            rating=rating)
                    return redirect('one:detail', product.slug)
            messages.error(self.request,'form is valid')
            return render(self.request, 'one_temp/content/comment.html',
                          {'form':form})
        form = CommentForm()
        return render(self.request, 'one_temp/content/comment.html',{'form':form,'product':product})

    def delete_comment(self,pk):
        if not self.request.user.is_authenticated:
            return redirect('one:login')
        comment = get_object_or_404(CommentProduct,id=pk)
        slug=comment.product.slug
        comment.delete()
        return redirect('one:detail' ,slug)

    def edit_comment(self,pk):
        if self.request.user.is_authenticated:
            comment = get_object_or_404(CommentProduct,id=pk,user=self.request.user)
            if self.request.method == 'POST':
                form = EditCommentForm(self.request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    comment.text = cd['text']
                    comment.rating = cd['rating']
                    comment.save()
                    return redirect('one:detail',comment.product.slug)
                else:
                    messages.error(self.request,'form is invalid')
                    return render(self.request,'one_temp/content/edit_comment.html',
                              {'form':form})
            else:
                form = EditCommentForm(initial={'text':comment.text,'rating':comment.rating})
                return render(self.request,'one_temp/content/edit_comment.html',
                          {'form':form})
        else:
            return redirect('one:login')






