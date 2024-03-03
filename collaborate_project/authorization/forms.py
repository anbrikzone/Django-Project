from django import forms
from .models import Users

class SignupForm(forms.ModelForm):
    first_name           = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name            = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    age                 = forms.IntegerField(label='', min_value = 18, max_value=80, widget=forms.TextInput(attrs={'placeholder': 'Age'}))
    email               = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    login               = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    password            = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password_confirm    = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    
    class Meta:
        model   = Users
        fields  = ['first_name', 'last_name', 'age', 'email', 'login', 'password', 'password_confirm']

class SigninForm(forms.ModelForm):
    login       = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    password    = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
    class Meta:
        model   = Users
        fields  = ['login', 'password']