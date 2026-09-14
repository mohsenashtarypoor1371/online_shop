from django.db import models
from django.contrib.auth.models import User
from first_app.models import Product
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=11)
    address = models.TextField(max_length=250)
    create = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100,null=True,blank=True)
    STATUS_CHOICE =[('pending','Pending'),('draft','Draft'),('paid','Paid'),
                    ('sent','Sent'),('delivered','Delivered')]
    status = models.CharField(max_length=20,choices=STATUS_CHOICE,default='draft')

    def __str__(self):
        return f'{self.name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f'{self.product}'