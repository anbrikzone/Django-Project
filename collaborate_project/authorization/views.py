from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignupForm, SigninForm

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
            username = request.POST.get("username")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            email = request.POST.get("email")
            # Check if passwords are equal
            if password1 == password2:
                # Check if username or email have already exist in database
                if not User.objects.filter(email = email) and not User.objects.filter(username = username):
                    register = form.save()
                    login(request, register)

                    # check if groups have been created
                    if not Group.objects.filter(name = 'user').exists() and not Group.objects.filter(name = 'admin').exists():
                        Group.objects.create(name = 'user')
                        Group.objects.create(name = 'admin')

                    return redirect('/projects')
                else:
                    messages.error(request, "The email or username have been already used.") 
            else:
                messages.error(request, "Passwords fields are not equal.") 
    context = {
        'title': "Sign up",
        'header': "Register Form",
        'form': form
        }
    return render(request, "authorization/signup.html", context=context)

# Allow to signin in our app
def signin(request):
    # If user has already authenticated just redirect him on the main page
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
                messages.error(request, "There is no such user in the system.")
    
    context = {
        'title': "Sign in",
        'header': "Sign in",
        'form': form
        }
    return render(request, "authorization/signin.html", context=context)

# Profile
def profile(request):
    # If user is superuser redirect him to django admin panel
    if request.user.is_superuser:
        return redirect('/admin')
    else:
        users = User.objects.filter(id = request.user.id)
        context = {
            'title': "Profile",
            'header': "Profile",
            'users': users,
            }
        return render(request, "authorization/profile.html", context=context)

# Logout
def mylogout(request):
    logout(request)
    return redirect("/")