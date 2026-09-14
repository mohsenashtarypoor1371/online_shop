from django.db import models
from first_app.models import User,Product

# Create your models here.

class CartList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product =models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user','product']

    def __str__(self):
        return f'{self.user}-{self.product}'