from django.contrib import admin
from . models import CartList

# Register your models here.

class AdminCart(admin.ModelAdmin):
    list_display = ['user','product','quantity','create']
admin.site.register(CartList)