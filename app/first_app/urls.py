from django.conf import settings
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'first_app'

urlpatterns = ([path('',views.index,name=''),
                path('product/',views.product_,name='product'),
                path('contact/',views.contact_us,name='contact'),
                path('cooperation/',views.cooperation_,name='cooperation'),
                path('detail/<slug:slug>/',views.detail_product,name='detail'),
                path('comment/<slug:slug>/',views.comment_product,name='comment'),
                path('search/',views.search,name='search'),
                path('tag/<slug:slug>/',views.tag_detail,name='tag'),
                path('login/',views.login_user,name='login'),
                path('sign_up/',views.sign_up,name='sign_up'),
                path('log_out/',views.log_out,name='log_out'),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)+
               static(settings.STATIC_URL,document_root = settings.STATIC_ROOT))