from django.db import models
from django.contrib.auth.models import User
from one.models import Product
# Create your models here.

class Order(models.Model):
    CHOICES_STATUS = (('paid','PAID'),('pending','PENDING'),('not access','not_access'),
                      ('not delivered','not_delivered'),('delivered','DELIVERED'),('processing','PROCESSING'))
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=11)
    address = models.TextField()
    status = models.CharField(choices=CHOICES_STATUS,default='pending', max_length=20)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)