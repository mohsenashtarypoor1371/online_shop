from django.contrib import admin

# Register your models here.
from .models import Order,OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ['name','phone','address','status']
admin.site.register(Order)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['quantity','price',]
admin.site.register(OrderItem)