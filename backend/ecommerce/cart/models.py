from django.db import models
from django.contrib.auth.models import User


from myapp.models import *
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.PositiveIntegerField(default=0)
    price = models.CharField(max_length=200)
    
