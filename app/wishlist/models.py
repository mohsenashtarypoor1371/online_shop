from django.db import models
from first_app.models import User,Product
# Create your models here.

class WishList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','product')
        ordering = ['-created']

    def __str__(self):
        return f'{self.user}-{self.product}'
