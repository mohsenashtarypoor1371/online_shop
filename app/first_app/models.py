from django.contrib.gis.gdal.prototypes.ds import set_spatial_filter
from django.db import models
from django.db.models import CASCADE
from django.db.transaction import savepoint
from django.template.context_processors import request
from django.utils.text import slugify
from django.contrib.auth.models import User
from psycopg2.errorcodes import TRANSACTION_ROLLBACK


class Category(models.Model):
    product_name= models.CharField(max_length=25)
    product_type = models.CharField(max_length=25)
    slug = models.SlugField(unique=True,null=True,blank=True)
    def save(self,*args,**kwargs):
        if not self.slug and self.product_name:
            slug_base = slugify(self.product_name)
            slug = slug_base
            num = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f'{slug_base}{num}'
                num += 1
                self.slug =slug
        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.product_name}-{self.product_type}'


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(unique=True,blank=True)
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=20)
    description = models.CharField(max_length=150,blank=True)
    price = models.PositiveBigIntegerField()
    discount_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    image = models.ImageField(upload_to='products_image',blank=True,null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    tag = models.ManyToManyField(Tag,blank=True)
    stock = models.PositiveSmallIntegerField(default=0)
    def final_price(self):
        if self.discount_price:
            return self.discount_price
        else:
            return self.price

    def save(self,*key,**kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*key,**kwargs)
    def __str__(self):
        return self.product_name

class ContactUs(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    criticisms = models.TextField()
    email = models.EmailField()
    subject = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def  __str__(self):
        return self.first_name

class Cooperation(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    email = models.EmailField(blank=False,null=False)
    job_title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name} {self.email}'

class DetailProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=25)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    color = models.CharField(max_length=10)
    manufacturer_country = models.CharField(max_length=10)
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class CommentProduct(models.Model):
    product =models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    name_user = models.CharField(max_length=25)
    email_user = models.EmailField(blank=True,null=True)
    picture_user = models.ImageField(upload_to='products_image',blank=True,null=True)
    comment_user = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name_user}:{self.comment_user}"

