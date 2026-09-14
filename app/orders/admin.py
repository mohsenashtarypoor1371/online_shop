from django.contrib import admin
from . models import *
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user']
admin.site.register(Order)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product']
admin.site.register(OrderItem)