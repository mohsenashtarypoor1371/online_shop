import site

from django.contrib import admin
from . models import WishList
# Register your models here.

admin.site.register(WishList)
class WishAdmin(admin.ModelAdmin):
    list_display = ['user','product']
