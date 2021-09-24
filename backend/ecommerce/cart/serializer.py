from django.db.models import fields
from rest_framework import exceptions, serializers
from. models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['id','user','product','quantity','total','price']