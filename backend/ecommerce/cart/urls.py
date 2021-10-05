from django.db import router
from django.urls import path
from rest_framework import views
from . import views 


urlpatterns=[
    # path('cart/',views.cart,name="cart"),
    path('cartdata/<int:pk>',views.cart_data,name="cartdata"),
    path('deletecart/<int:pk>',views.delete_cart_product,name="deletecart"),
    path('getcartdata/',views.get_cart_details,name="getcartdata"),
]