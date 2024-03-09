from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project

@login_required(login_url="/signin")
def index(request):
    all_projects = ""
    shared_projects = ""
    
    context = {
        'title': "Projects",
        'header': "Projects",
        }

    return render(request, 'projects/index.html', context=context)

def add_project(request):
    pass

def edit_project(request):
    pass