from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from myapp.models import *

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price']

