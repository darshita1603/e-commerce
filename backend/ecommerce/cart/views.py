from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from rest_framework.serializers import Serializer

# Create your views here.

from django.contrib.auth.models import User
from.models import *
from rest_framework.response import Response
from django.contrib.auth import login as django_login,logout as django_logout
from rest_framework.response import Response
from rest_framework import status
from.serializer import*
from django.http.response import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET',"POST"])
@permission_classes([IsAuthenticated])
def cart(request):
    if request.method=='GET':
        token=request.user.auth_token
        user=request.user
        cart_data=Cart.objects.filter(user__username=user)
        print(cart_data,"dataaaa")
        serializer=CartSerializer(cart_data,many=True)
        print(serializer,"sssssssssssss")
        return Response(serializer.data)

    if request.method=='POST':
        token=request.user.auth_token
        # print(token)
        serializer=CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

def cart(request):
    print("kkkkkk")
    return render(request,"cart/cart.html")
