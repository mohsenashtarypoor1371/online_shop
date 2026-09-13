from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name='one'
urlpatterns=([path('',views.shop_show,name='shop_show'),
              path('detail/<slug:slug>/',views.detail_pro,name='detail'),
              path('search/',views.search,name='search'),
              path('contact/',views.contact,name='contact'),
              path('login/',views.login,name='login'),
              path('sign_up/',views.sign_up,name='sign_up'),
              path('log_out/',views.log_out,name='log_out'),
              path('recruitment/',views.recruitment,name='recruitment'),
              path('comment/<slug:slug>/', views.comment_product, name='comment'),
              path('delete_comment/<int:pk>/',views.delete_comment,name='delete_comment'),
              path('edit_comment/<int:pk>/',views.edit_comment,name='edit_comment'),



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+
             static(settings.STATIC_URL,document_root=settings.STATIC_ROOT))