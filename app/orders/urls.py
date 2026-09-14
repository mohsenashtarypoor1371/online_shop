from django.urls import path
from . import views

app_name='orders'

urlpatterns= [path('<int:pk>/',views.show_order,name='show_order'),
              path('order/',views.order,name='order'),
              path('order_item/',views.order_item,name='order_item'),
              path('my_order/',views.my_order,name='my_order'),
              path('remove/<int:pk>',views.remove,name='remove'),
              path('final_order/',views.final_order,name='final_order'),
              path('payment/',views.payment,name='payment'),
              path('product_paid',views.product_paid,name='product_paid'),
              path('detail_paid/<int:pk>',views.detail_paid,name='detail_paid'),




]