from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, ProjectMember

from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.db.models import F, OuterRef, Subquery

@login_required(login_url="/signin")
def index(request):
    all_projects = Project.objects.all().order_by('-created')
    shared_projects = Project.objects.filter(projectmembers__users__id = request.user.id).order_by('-created')
    # my_projects = Project.objects.filter(owner_id = request.user.id).order_by('-created')

    my_projects = Project.objects.raw(f'''select
                pp.id
                , pp.name
                , pp.description
                , pp.created
                , group_concat(au.username, ', ') as users 
                from projects_project pp 
                left join projects_projectmember ppm on pp.id = ppm.projects_id 
                left join auth_user au ON au.id = ppm.users_id
                where pp.owner_id = %s''', [request.user.id])
    
    context = {
        'title': "Projects",
        'header': "Projects",
        'all_projects': all_projects,
        'shared_projects': shared_projects,
        'my_projects': my_projects,
        }

    return render(request, 'projects/index.html', context=context)

@login_required(login_url="/signin")
def add_project(request):
    
    if request.method == 'POST':
        project_name = request.POST.get("project_name")
        project_description = request.POST.get("project_description")

        form = Project.objects.create(name = project_name, description = project_description, owner = request.user)
        form.save()

        return redirect("index")
    
    context = {
        'title': "Projects",
        'header': "Projects",
        }
    return render(request, 'projects/add_project.html', context=context)

@login_required(login_url="/signin")
def edit_project(request, id):

    if request.method == 'POST':
        project_name = request.POST.get("project_name")
        project_description = request.POST.get("project_description")

        form = Project.objects.get(pk = id)
        form.name = project_name
        form.description = project_description
        form.save()

        return redirect("index")

    project = Project.objects.get(pk = id)
    context = {
        'title': "Projects",
        'header': "Projects",
        'project': project,
        }
    return render(request, 'projects/edit_project.html', context=context)

@login_required(login_url="/signin")
def remove_project(request, id):
    Project.objects.filter(id = id).delete()
    return redirect("index")