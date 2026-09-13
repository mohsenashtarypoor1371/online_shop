from django.contrib import admin
from . models import *
class CategoryAdmin(admin.ModelAdmin):
     list_display = ['name']
admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
     list_display = ['category','product_name','price','stock','manufacture_country']
admin.site.register(Product)

class ContactAdmin(admin.ModelAdmin):
     list_display = ['f_name','l_name','email','subject']
admin.site.register(Contact)

class RecruitmentAdmin(admin.ModelAdmin):
     list_display = ['f_name','l_name','email','phone']
admin.site.register(Recruitment)

class CommentProductAdmin(admin.ModelAdmin):
     list_display = ['user','product','text']
admin.site.register(CommentProduct)