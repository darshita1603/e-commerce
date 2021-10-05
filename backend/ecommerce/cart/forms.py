from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from myapp.models import *

class UserUpdateForm(forms.ModelForm):
    class Meta:
        models=Profile
        fields=['first_name','last_name','mobileno','city','state','address','pincode']