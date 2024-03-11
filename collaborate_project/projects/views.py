from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, ProjectMember
from django.contrib import messages

@login_required(login_url="/signin")
def index(request):
    all_projects = Project.objects.all().order_by('-created')
    shared_projects = Project.objects.filter(projectmembers__users__id = request.user.id).order_by('-created')
    # my_projects = Project.objects.filter(owner_id = request.user.id).order_by('-created')

    my_projects = Project.objects.raw(f'''select 
                pp.id
                , pp.name
                , pp.description
                , owner_id
                , pp.created
                , group_concat(au.username, ', ') as users
                from projects_project pp 
                left join projects_projectmember ppm on pp.id = ppm.projects_id
                left join auth_user au on au.id = ppm.users_id
                where pp.owner_id = %s
                group by pp.id''', [request.user.id])
    
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
        if request.POST.get("EditProject"):
            project_name = request.POST.get("project_name")
            project_description = request.POST.get("project_description")

            form = Project.objects.get(pk = id)
            if form is not None:
                form.name = project_name
                form.description = project_description
                form.save()

                return redirect("index")
        
        elif request.POST.get("RemoveMember"):
            member_id = request.POST.get("select_members")
            ProjectMember.objects.filter(projects__id = id, users__id = member_id).delete()
            return redirect(request.META.get('HTTP_REFERER'))

        elif request.POST.get("Invite"):
            project_name = request.POST.get("project_name")
            email_member = request.POST.get("email_member")
            member = User.objects.get(email = email_member)
            project = Project.objects.get(id = id)
            project_memeber = ProjectMember.objects.filter(projects__id = id, users__id = member.id)
            if project_memeber:
                messages.error(request, f"The user with email {email_member} has already been added as a member for the project {project_name}")
            else:
                project_memeber = ProjectMember.objects.create(projects = project, users = member)
                project_memeber.save()
            
            return redirect(request.META.get('HTTP_REFERER'))
        
    project = Project.objects.get(pk = id)
    members = User.objects.filter(projectmember__projects__id = id).values_list('id', 'username')
    context = {
        'title': "Projects",
        'header': "Projects",
        'project': project,
        'members': members,
        }
    return render(request, 'projects/edit_project.html', context=context)

@login_required(login_url="/signin")
def remove_projectmember(request, id):
    if request.method == 'POST':
        member_id = request.POST.get("select_members")
        print(member_id)
        ProjectMember.objects.filter(projects__id = id, users__id = member_id).delete()
        return redirect("index")

@login_required(login_url="/signin")
def remove_project(request, id):
    Project.objects.filter(id = id).delete()
    return redirect("index")