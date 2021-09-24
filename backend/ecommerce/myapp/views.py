from django.shortcuts import redirect, render
from rest_framework.serializers import Serializer

# Create your views here.
from.serializer import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import login as django_login,logout as django_logout
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from django.http.response import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "register.html"

    def get(self,request):
        return Response({"message":"Register Successfully"})

    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect('login')
    
    

class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "login.html"
    # user_param_config=openapi.Parameter('username',in_=openapi.IN_QUERY,description="Description",type=openapi.TYPE_STRING)
    # password_param_config=openapi.Parameter('password',in_=openapi.IN_QUERY,description="Description",type=openapi.TYPE_STRING)
    # @swagger_auto_schema(manual_parameters=[user_param_config,password_param_config])
   
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        django_login(request,user)

        session_user=User.objects.filter(username=self.request.data['username']).first()
        print(session_user,"ttttttttttttttttt")
        token,created=Token.objects.get_or_create(user=user)
        request.session['user_token']=token.key
        print(request.session['user_token'],"ooooooooooooooooooooooooooooo")

        request.session['user_id']= session_user.id
        print(request.session['user_id'],"ggggggggggggggggggggggggggggg")
        # return Response({"message":"login Successfully","token":token.key},status=200)
        return redirect('dashboard')
        
    
    def get(self,request):
        return Response({"message":"login Successfully"})

@permission_classes([IsAuthenticated])
class LogOutView(APIView):
    def get(self,request):
        try:  
            request.user.auth_token.delete()
            django_logout(request)
            return Response({"message":"logout Successfully"},status=204)
        except request.user.auth_token.DoesNotExist:
             return HttpResponse({"message":"Please check token is not valid"},status=status.HTTP_400_BAD_REQUEST)


def dashboard(request):
    product=Product.objects.all()
    print(product,"uuuuuuuuuu")
    return render(request,"dashboard.html",{'products':product})


@api_view(['GET',"POST"])
def product(request):
    if request.method=='GET':
        print("kkkkkkkk")
        product=Product.objects.all()
        serializer=ProductSerializer(product,many=True)
        print(serializer,"sssssssssssss")
        return Response(serializer.data)

    if request.method=='POST':
        serializer=ProductSerializer(data=request.data)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 


def product_details(request,pk):
    product=Product.objects.get(pk=pk)
    user = User.objects.get(id=pk)
    print(user,"iiiii")
    #do something with this user
    print(product,"ppppppppppppppp")
    return render(request,"product_details.html",{'products':product})

# create bid api........


@api_view(["POST"])
def bid(request):
    # if request.method=='GET':
    #     print("rrrrrrrrrrrrrr")
    #     product=Bid.objects.get(pk=pk)
    #     serializer=BidSerializer(product)
    #     print(serializer,"sssssssssssss")
    #     return Response(serializer.data)
    # bid_data=Bid.objects.get()
    if request.method =="POST":
       serializer=BidSerializer(data=request.data)
       if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    # return render(request,"bid.html")

def bid_data(request,pk):    
    print(request.POST,pk)
    if request.method=="POST":
        # serializer=ProductSerializer(data=request.data,many=True)
        # print(serializer,"iiiiiiiiiiiiiiii")
        print("5555555555555")
        print("77777777777777")
        print(request.user)
        # print(request.product)
        data=Bid.objects.filter(user=request.user).first()
        print(data.product.id)

        context={
            "user":request.user.id,
            "product":data.product.id,
            "price":request.POST["price"]

        }     
        serializers=BidSerializer(data=context)
        if serializers.is_valid():
            serializers.save()
        # print(serializers)
        # user = User.objects.get(id=pk)
        # print(user,"iiiii")
        # product=Product.objects.filter(user=request.user).first()
        # print(product,"00000000000000000")
       
        return redirect("singleproductdetail",pk=pk)
    return render(request,"bid.html")