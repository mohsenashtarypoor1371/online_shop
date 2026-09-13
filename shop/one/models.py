from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name_product = models.CharField(max_length=25)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    stock = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True,blank=True)
    manufacture_country = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = models.ImageField()

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name_product)
        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.name_product}{self.manufacture_country}'


class Contact(models.Model):
    f_name = models.CharField(max_length=25)
    l_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=25)
    message = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering=['create']
    def __str__(self):
        return f'{self.f_name}{self.l_name}'

class Recruitment(models.Model):
    f_name = models.CharField(max_length=25)
    l_name = models.CharField(max_length=25)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    job_title = models.CharField(max_length=25)
    skill = models.TextField()
    work_history = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-create_at']

    def __str__(self):
        return f'{self.f_name}{self.l_name}{self.skill}'

class CommentProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=250)
    rating = models.PositiveIntegerField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return f'{self.user}-{self.product}'