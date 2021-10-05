from django.shortcuts import redirect, render,get_object_or_404
from rest_framework.serializers import Serializer
from django.core import validators
# Create your views here.
from.serializer import *
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import login as django_login,logout as django_logout
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from django.http.response import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from myapp.forms import *
from cart.models import *
from django.db.models import Max

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

def Logout(request):
    request.user.auth_token.delete()
    django_logout(request)
    return render(request,"login.html")

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
    bid_users=[]
    bid_data=[]
    product=Product.objects.get(pk=pk)
    user = User.objects.get(id=pk)
    print(user.id)
    get_user=Bid.objects.filter(product=product.id)
    print(get_user)
    get_all_price=list(Bid.objects.filter(product=product.id).values_list('price',flat=True))
    print(get_all_price,"ritaaaaaaaaaaaaaaaa")
    
    for i in  get_user:
        bid_user=i.user
        bid_users.append(bid_user)
  
    if request.user in bid_users:
        bid_users.remove(request.user)
        show_userdata=bid_users
        # print(show_userdata,"999999")
    
    try:
        for i in show_userdata:
            bid_data_users=i.first_name
            print(bid_data_users,"ppppp")
            bid_data.append(bid_data_users)
            bid_data.sort(reverse=True)
        print(bid_data,"ioioio")
    except:
        pass

    if not get_all_price:
        return render(request,"product_details.html",{'products':product,'userdata':bid_data})
    else:
        max_value=max(get_all_price)
        context={
            'products':product,
            'max_value':max_value,
            'userdata':bid_data
        }
        return render(request,"product_details.html",context)

# create bid api........


@api_view(["POST"])
def bid(request):
    if request.method =="POST":
       serializer=BidSerializer(data=request.data)
       if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    # return render(request,"bid.html")

@api_view(["GET"])
def bid_get(request,pk):
    if request.method=="GET":
        bid=Bid.objects.get(pk=pk)
        user=User.objects.get(id=pk)
        print(user)
        serializer=BidSerializer(bid)
        print(serializer,"ppppppppppppppp")
        # print(serializer.data,"datttaa")
        return Response(serializer.data)

@api_view(["PUT"])
def bid_update(request,pk):
    if request.method=="PUT":
        bid=Bid.objects.get(pk=pk)
        product=Product.objects.get(pk=pk)
        user = User.objects.get(id=pk)
        print(user)

        data={
            "user":user.id,
            "product":product.id,
            "price":request.data['price']

        }   
        serializer=BidSerializer(bid,data=data)
        if  serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 


def bid_updatedata(request, pk):
   user = request.user.id
   print(user)
   products = Product.objects.get(pk=pk)
   print(products.id)
   product = Bid.objects.filter(user=user, product=products).first()
   
   form = UserUpdateForm(request.POST or None, instance=product)
   
   if form.is_valid():
       form.save()
       print("ooojojoijok")
       form=UserUpdateForm(request.POST) 
       return redirect("singleproductdetail",pk=pk)
   return render(request,'update_bid.html',{"form":form})

def bid_data(request,pk):    
    print(request.POST,pk)
    if request.method=="POST":

        # user_data=[]
        # product_data=[]
        # serializer=ProductSerializer(data=request.data,many=True)
        # print(serializer,"iiiiiiiiiiiiiiii")
        print("5555555555555")
        print("77777777777777")
        print(request.user.id)
        # print(request.product)
        # data=Bid.objects.filter(user=request.user).first()
        # print(data.product.id)
        
        product=Product.objects.get(pk=pk)
        user = User.objects.get(email=request.user.email)
        print(user)
        # product=Product.objects.get(pk=pk)
        # print(product,"77777777777777777777")
        # user = User.objects.get(id=pk)
        pro_price=product.price

        bid_price=int(request.POST["price"])
        print(bid_price)
      
        context={
            "user":user.id,
            "product":product.id,
            "price":request.POST["price"]

        }   
        # print(product.id,"iiiiiiiiitttttttttttttttt")
        # data1=list(Bid.objects.filter(product=product.id).values_list('price',flat=True))
        # print(data1,"ritaaaaaaaaaaaaaaaa")
        
        # product_bid=list(Bid.objects.filter(product=product.id).values_list('product',flat=True))
        # print(product_bid)
       
        # user_bid=list(Bid.objects.filter(user=user.id).values_list('user',flat=True))
        # print(user_bid,"nii")
        
        bidObj = Bid.objects.filter(user=user.id,product=product.id)
        print(bidObj)
        
        if bidObj.exists():
            print("jjjjj")
            messages.error(request,f'Please you should only one time Bid')
            return redirect("biddata",pk=pk)

        else:
            if bid_price > pro_price:
                    serializers=BidSerializer(data=context)
                    serializers.is_valid()
                    serializers.save()
                    return redirect("singleproductdetail",pk=pk)
            else:
                # raise django.forms.ValidationError(_('Enter a valid price.'))
                messages.error(request,f'Please Enter Valid Bid Price')
                return redirect("biddata",pk=pk)
                
           
        # print(serializers)
        # user = User.objects.get(id=pk)
        # print(user,"iiiii")
        # product=Product.objects.filter(user=request.user).first()
        # print(product,"00000000000000000")
       
        # return redirect("singleproductdetail",pk=pk)
    return render(request,"bid.html")


    
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

def checkout(request,pk):
    print(pk,"pkkkk")
    products=[]
    user=request.user
    cart_data=list(Cart.objects.filter(user__username=user).values_list('product_id',flat=True))
    cart=Cart.objects.filter(user__username=user)
    print(cart)
    print(cart_data,"carttt")
    total=0
    quantity=1
    products_length=len(cart_data)
    

    for i in cart:
        total = float(i.price) + total
        price=i.price
        quantity=i.quantity * products_length


    for i in cart_data:
        product=Product.objects.get(pk=i)
        products.append(product)
    # print(user.id,"userid")
    # print(product.id)
    if request.method =="POST":
        print(request,"hrrrr")

        data={
           "user":user.id,
           "product":product.id,
           "first_name":request.POST['firstname'],
           "last_name":request.POST['lastname'],
           "mobileno":request.POST["mobileno"],
           "city":request.POST["city"],
           "state":request.POST["state"],
           "address":request.POST["address"],
           "pincode":request.POST["postcode"]          
        }

        product_pro=list(Profile.objects.filter(product=product.id).values_list('product',flat=True))
        
        user_pro=list(Profile.objects.filter(user=user.id).values_list('user',flat=True))
        print(user_pro,"okokok")

        if user.id in user_pro and product.id in product_pro:
            messages.error(request,f'Please Update your data....Enter Only one time data')
            return redirect("checkout",pk=pk)
        else:
           serializer=CheckOutSerializer(data=data)
           if serializer.is_valid():
               serializer.save()
               return redirect('paymentdata')
        
    return render(request,"checkout/checkout.html",{'products':products,'total':total,'quantity':quantity})

@api_view(["POST"])
def check(request):
   if request.method =="POST":
       serializer=CheckOutSerializer(data=request.data)
       print(serializer)
       if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

# def edit_checkout(request):
#     user=request.user
#     print(user,"kk")
#     user_data=Profile.objects.filter(user__username=user)
#     print(user_data)
#     form = EditUpdateForm(request.POST or None, instance=user_data)
#     print(form)
#     print(request.method)
    # user_data=Profile.objects.filter(user__username=user)
    # print(user_data)
    
    # for i in user_data:
    #     first_name=i.first_name
    #     print(first_name,"ffffffff")
    #     last_name=i.last_name
    #     mobile_no=i.mobileno
    #     city=i.city
    #     state=i.state
    #     address=i.address
    #     pincode=i.pincode

    # context={
    #     'userid':user.id,
    #     "first_name":first_name,
    #     "last_name":last_name,
    #     "mobile_no":mobile_no,
    #     "city":city,
    #     "state":state,
    #     "address":address,
    #     "pincode":pincode,
    # }
    # return render(request,"checkout/edit_details.html",context)

   
def edit_checkout(request,pk):
        user = User.objects.get(id=pk)
        print(user.id,"kkk")
        user_data=Profile.objects.filter(user__username=user).first()
        print(user_data,"pppppp")

        # for i in user_data:
        #     print(i,"[[[[[[[[")
        #     print(i.first_name)
        #     print(i.product_id)
        # data_list = get_object_or_404(User,id=pk)
        # print(data_list,"444444444444")
        form = ProfileForm(request.POST or None, instance=user_data)
        print(form)
        if form.is_valid():
            print("pppppiodsade")
            form.save()
            print("ooojojoijok")
            form=ProfileForm(request.POST)
            return redirect("paymentdata")
        return render(request,'checkout/edit_details.html',{"form":form})

