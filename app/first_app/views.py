from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import password_changed
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from wishlist.models import WishList
from . models import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q,Sum
from .form import *
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchRank,SearchQuery,SearchVector
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.views.decorators.cache import never_cache
from wishlist.models import WishList


def index(request):
    return render(request,'html/first.html')

@never_cache
def product_(request):
    product = Product.objects.annotate(g = Sum('detailproduct__price'))
    total_price_all = Product.objects.aggregate(total_price_all1=Sum('detailproduct__price'))
    user = request.user
    paginator = Paginator(product,2)
    page = request.GET.get('page',1)
    try:
        page  = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request,'html/product.html',context={'product':product,'page':page,
                                                       'total_price_all':total_price_all,
                                                       'user':user})

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your information and comments have been successfully save')
            return redirect('first_app:contact')
        else:
            return HttpResponse('form is invalid')
    else:
        form = ContactForm()
        return render(request,'form/contact.html',context={'form':form})

def cooperation_(request):
    if request.method == 'POST':
        form = CooperationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            phone = cd['phone']
            email = cd ['email']
            job_title = cd['job_title']
            description = cd['description']
            message = (f'{name} to {phone} and {email} the job  {job_title}'
                       f'has activity and is description he job{description}')
            send_mail('job_title',message,email,['ashtarypoormohsen@gmail.com'],fail_silently=False)
            form.save()
            messages.success(request, 'message saved successfully')
            return redirect('first_app:cooperation')
        else:
            messages.error(request, 'message invalid')
            form =ContactForm()
            return render(request, 'form/cooperation.html', {'form': form})
    else:
        form = CooperationForm()
        return render(request,'form/cooperation.html',{'form':form})

def detail_product(request,slug):
    product = get_object_or_404(Product,slug=slug)
    detail_pro = DetailProduct.objects.filter(product=product)
    comment2 = CommentProduct.objects.filter(product=product).order_by('create_at')

    return render(request,'html/detail.html',{'product':product,

                                              'detail_pro':detail_pro,'comment2':comment2})

def comment_product(request,slug):
    product = get_object_or_404(Product,slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            name_user = cd['name_user']
            email_user = cd['email_user']
            picture_user = cd['picture_user']
            comment_user = cd['comment_user']
            comment1 = CommentProduct(product=product,user=request.user,name_user=name_user,email_user=email_user,
                                      picture_user=picture_user,comment_user=comment_user)
            comment1.save()
            return redirect('first_app:product')
        form =CommentForm()
        return render(request,'html/comment.html',{'form':form})
    form = CommentForm()
    return render(request, 'html/comment.html', {'form': form})

# def search(request,):
#     query = request.GET.get('query')
#     if query:
#         product = Product.objects.filter(Q(product_name__icontains=query)|Q(description__icontains=query))
#         return render(request, 'html/search.html', context={'product': product, 'query': query})
#     elif not query:
#         messages.error(request,'Enter the product in the search.')
#         return redirect('first_app_temp:product')
#     elif not product.exists():
#         messages.error(request,'this product does not exist')
#         return render(request,'html/product.html')

def search(request):
    query = request.GET.get('query')
    if query:
        vector = SearchVector('product_name','description')
        search_query = SearchQuery(query)
        search_rank = Product.objects.annotate(rank=SearchRank(vector,search_query)).filter(Q(rank__gte=0.1)
                                                                                           |Q(product_name__icontains=query)
                                                                                           |Q(description__icontains=query))
        return render(request, 'html/search.html', context={'search_rank':search_rank})

    elif not query:
        messages.error(request,'Enter the search term again.')
        return redirect('first_app:product')
    elif not query.exists():
        messages.error(request,'There is no product')
        return render(request, 'html/product.html')

def tag_detail(request,slug):
    tag = get_object_or_404(Tag,slug=slug)
    product = Product.objects.filter(tag=tag).distinct()
    context = {'product':product,'tag':tag}
    return render(request,'html/detail.html',context=context)

@never_cache
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password = cd['password'])
            if user is not None:
                if user.is_active:
                        login(request,user)
                        return redirect('first_app:product')
                else:
                    return HttpResponse('user is not active')
            messages.error(request,'password in valid')
            return render(request,'login/login_user.html',context={'form':form})
        return render(request,'login/login_user.html',context={'form':form})
    form =LoginForm()
    return render(request,'login/login_user.html',context={'form':form})

def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            email = cd['email']
            if User.objects.filter(username=username).exists():
                messages.error(request,'user exists')
                return render(request,'login/sign_up.html',)
            else:
                user = User.objects.create_user(username=username,password=password,email=email)
                messages.success(request,'signup successful')
                return redirect('first_app:product')
        return render(request,'login/sign_up.html',context={'form':form})
    form = SignupForm()
    return render(request, 'login/sign_up.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('/')

