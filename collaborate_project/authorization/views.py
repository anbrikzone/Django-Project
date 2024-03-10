from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignupForm, SigninForm
# from .models import Users, Roles

# This method shows main page
# If user is not authorized function return signin/registraion form
# if user is authorized then function redirect him to project's index page
def index(request):
    return render(request, "authorization/index.html")

# This method by default return register page
# If pressed "Sign Up" button then run block of code responsible for handler of registration
def signup(request):
    if request.user.is_authenticated:
        return redirect('/projects')
    form = SignupForm()
    
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 == password2:
                register = form.save()
                login(request, register)
                return redirect('/projects')
            else:
                messages.error(request, "Passwords fields are not equal.") 
    context = {
        'title': "Sign up",
        'header': "Register Form",
        'form': form
        }
    return render(request, "authorization/signup.html", context=context)

def signin(request):
    if request.user.is_authenticated:
        return redirect('/projects')
    form = SigninForm()
    if request.method == "POST":
        form = SigninForm(request, request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/projects')
            else:
                messages.error("There is no such user in the system.")
    
    context = {
        'title': "Sign in",
        'header': "Sign in",
        'form': form
        }
    return render(request, "authorization/signin.html", context=context)

def profile(request):
    context = {
        'title': "Profile",
        'header': "Profile",
        }
    return render(request, "authorization/profile.html", context=context)

def mylogout(request):
    logout(request)
    return redirect("/")