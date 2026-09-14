from django.urls import path
from cart import views
app_name='cart'

urlpatterns = [path('',views.show_cart,name='show_cart'),
               path('add/<int:pk>',views.add_cart,name='add'),
               path('delete/<int:pk>',views.delete_cart,name='delete'),
               path('update/<int:pk>',views.update_cart,name='update'),
               path('total/',views.total_price,name='total'),
               path('total_quantity/',views.total_quantity,name='total_quantity'),
               path('total_price_all/',views.total_price_all,name='total_price_all'),
               path('login_cart/',views.login_cart,name='login_cart'),


]