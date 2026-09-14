from django.urls import path
from . import views
app_name = 'wishlist'

urlpatterns = [
    path('wish_list/',views.wish_list,name='wish_list'),
    path('add_wish/<int:pk>/',views.add_wish,name='add_wish'),
    path('remove/<int:pk>/',views.remove,name='remove'),

]