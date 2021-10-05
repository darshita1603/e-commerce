
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from rest_framework.serializers import Serializer
from django.contrib import messages  
from django.shortcuts import render,get_object_or_404,redirect
# Create your views here.
from django.urls import reverse
from django.contrib.auth.models import User
from.models import *
from rest_framework.response import Response
from django.contrib.auth import login as django_login,logout as django_logout
from rest_framework.response import Response
from rest_framework import status
from.serializer import*
from django.contrib.auth.decorators import login_required
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

# def cart_data(request,pk):
#     product_details=[]
#     token=request.user.auth_token
#     user=request.user
#     print(user)
#     cart_data=list(Cart.objects.filter(user__username=user))
#     print(cart_data,"09090909")

#     for i in cart_data:
#         print(i.product.id)
#         p1 = Product.objects.get(pk=i.product.id)
#         product_details.append(p1)
        
#     print(product_details)
    
#     return render(request,"cart/cart.html",{'products':product_details})
@login_required
def cart_data(request,pk):
    if request.method=="POST":
        print(request.method)
        token=request.user.auth_token
        user=request.user
        
        Userid = user
        product_details = get_object_or_404(Product, pk=pk)
        cid=Cart.objects.filter(user__username=user)

        Cart(user=Userid,product=product_details,price=product_details.price).save()
        return redirect("getcartdata")
        # return redirect(reverse('getcartdata',pk=user.id))

    else:
        cid=Cart.objects.filter(user__username=request.user)
        return render(request,"cart/getcartdata.html",{'products':cid})

@api_view(['DELETE'])
def delete_cart_product(request,pk):
    cart_product_details =get_object_or_404(Cart,pk=pk)
    cart_product_details.delete()
    return Response({"message":"Delete Successfully"},status=status.HTTP_204_NO_CONTENT)

def delete_cart_product(request,pk):
    cart_product_details =get_object_or_404(Cart,pk=pk)
    print(cart_product_details,"pppppppppppp")
    cart_product_details.delete()
    print("deleted")
    messages.success(request,f'Deleted Succesfully....!!!')
    return redirect("getcartdata")
    

def get_cart_details(request):
    user=request.user
    cart_data=Cart.objects.filter(user__username=user)
    print(user.id)
    print(cart_data)
    total=0
    for i in cart_data:
        total = float(i.price) + total
    
    return render(request,"cart/getcartdata.html",{'products':cart_data,'total':total,"userid":user.id})

       