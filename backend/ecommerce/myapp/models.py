from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Product(models.Model):
    model_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    image= models.ImageField(default='/profile_pics/default.jpg',upload_to='profile_pics')
    description = models.TextField() 
    car_published_year = models.CharField(max_length=200,default='')
    color=models.CharField(max_length=255)
    fuel_type=models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True)
    # expiry_date = models.DateTimeField()
 

class Bid(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9,decimal_places=2)


class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    mobileno=models.CharField(max_length=12)
    city=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    address=models.CharField(max_length=200)
    pincode=models.CharField(max_length=8)
    