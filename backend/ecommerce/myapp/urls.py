from django.db import router
from django.urls import path
from rest_framework import views
from .views import RegisterView,LoginView,LogOutView, product
from . import views 
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router=DefaultRouter()
router.register(r'register',RegisterView)

urlpatterns=[
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('dashboard/',views.dashboard,name="dashboard"),
    path('',views.dashboard,name="dashboard"),
    path('logout/',LogOutView.as_view()),
    path('logoutdata/',views.Logout,name="logoutdata"),
    path('product/',product,name="product"),
    path('product_details/',views.product_details,name="productdetails"),
    path('product_details/<int:pk>',views.product_details,name="singleproductdetail"),
    path('bid',views.bid,name="bid"),
    path('biddata/<int:pk>',views.bid_data,name="biddata"),
    path('bid_get/<int:pk>',views.bid_get,name="bidget"),
    path('bid_update/<int:pk>',views.bid_update,name="bidupdate"),
    path('bid_updatedata/<int:pk>',views.bid_updatedata,name="bidupdatedata"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)