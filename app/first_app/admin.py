from django.contrib import admin
from django.contrib.gis.gdal.prototypes.raster import set_ds_metadata_item

from . models import *
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['product_name']
admin.site.register(Category,CategoryAdmin)

admin.site.register(Product)
admin.site.register(Tag)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['description','price','product_name']
    list_display_links = ['product_name']
    list_editable = ('price',)

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['first_name' ,'last_name' ,'criticisms' ,'email','subject']
admin.site.register(ContactUs)

class CooperationAdmin(admin.ModelAdmin):
    list_display = ['name','phone','email','job_title','description','create_at']
admin.site.register(Cooperation)

class DetailAdmin(admin.ModelAdmin):
    list_display = ['category','name','price',
                    'description','color','manufacturer_country','type']
admin.site.register(DetailProduct)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name_user','email_user','picture_user','comment_user','create_at']
admin.site.register(CommentProduct)
