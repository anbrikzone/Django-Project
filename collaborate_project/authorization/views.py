from django.shortcuts import render
from django.http import HttpResponse

# This function shows main page
# If user is not authorized function return login/registraion form
# if user is authorized than function redirect him to projects index page
def index(request):
    return render(request, "authorization/index.html")

def signup(request):
    return render(request, "authorization/signup.html")

def login(request):
    return render(request, "authorization/login.html")