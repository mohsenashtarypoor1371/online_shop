from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [path('show_cart/',views.show_cart,name='show_cart'),
               path('add_cart/<int:pk>',views.add_cart,name='add_cart'),
               path('remove/<int:pk>',views.remove,name='remove'),
               path('update/<int:pk>/',views.update,name='update'),
               path('add_wish/<int:pk>',views.add_wish,name='add_wish'),
               path('delete/<int:pk>/',views.delete,name='delete'),
               path('show_wish/',views.show_wish,name='show_wish'),
               path('order/',views.order,name='order'),
               path('order_info/',views.order_info,name='order_info'),
               path('payment/',views.payment,name='payment'),
               path('payment_successful/',views.payment_successful,name='payment_successful'),
               path('payment_failed/',views.payment_failed,name='payment_failed'),
]