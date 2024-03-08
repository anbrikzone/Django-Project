from django import forms
# from .models import Users
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignupForm(UserCreationForm):
    first_name      = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name       = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username        = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    email           = forms.EmailField(label='', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1       = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2       = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    
    class Meta:
        model   = User
        fields  = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class SigninForm(AuthenticationForm):
    username    = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    password    = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
    # class Meta:
    #     model   = User
    #     fields  = ['username', 'password']