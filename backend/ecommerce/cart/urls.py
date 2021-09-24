from django.db import router
from django.urls import path
from rest_framework import views
from . import views 


urlpatterns=[
    path('cart/',views.cart,name="cart"),
    # path('cartdata/',views.cart_data,name="cartdata"),
]