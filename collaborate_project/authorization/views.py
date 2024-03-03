from django.shortcuts import render, redirect
from .forms import SignupForm, SigninForm
from .models import Users, Roles

# This method shows main page
# If user is not authorized function return signin/registraion form
# if user is authorized then function redirect him to project's index page
def index(request):
    return render(request, "authorization/index.html")

# This method by default return register page
# If pressed "Sign Up" button then run block of code responsible for handler of registration
def signup(request):
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            register = signup_form.save(commit=False)
            try:
                role_id  = Roles.objects.get(type="User")
            except:
                role = Roles.objects.create(type="User")
                role.save()
                role_id = Roles.objects.get(type="User")
            register.role = role_id
            register.save()
            return redirect('/projects')
    else:
        signup_form_initialize = SignupForm()
        context = {
            'title': "Sign up",
            'header': "Register Form",
            'form': signup_form_initialize
            }
        return render(request, "authorization/signup.html", context=context)

def signin(request):
    if request.method == "POST":
        signin_form = SigninForm(request.POST)
        if signin_form.is_valid():
            pass

    signin_form_initialize = SigninForm()
    context = {
        'title': "Sign in",
        'header': "Sign in",
        'form': signin_form_initialize
        }
    return render(request, "authorization/signin.html", context=context)