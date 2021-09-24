from django.db.models import fields
from rest_framework import exceptions, serializers
from. models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )   
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self,data):
        username=data.get('username','')
        password=data.get('password','')

        if username and password:
            user=authenticate(username=username,password=password)
        
            if user:
                if user.is_active:
                    data['user']=user
                else:
                    msg="user is deactivated"
                    raise exceptions.ValidationError(msg)
            else:
                msg="Password or Username is incorrect"
                raise exceptions.ValidationError(msg)

        else:
            msg="must be fill username and password"
            raise exceptions.ValidationError(msg)
        return data



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','user','model_name','brand','price','image',"description",'car_published_year','color','fuel_type']

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bid
        fields = ['user','product','price']