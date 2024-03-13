from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, ProjectMember
from django.contrib import messages

# Main page of our project
# login_required check if user is authenticated, otherwise redirect him on log in page
@login_required(login_url="/signin")
def index(request):
    # Collect data for all created projects
    all_projects = Project.objects.all().order_by('-created')
    # Filter projects which have been shared with the user and order them by date of creating
    shared_projects = Project.objects.filter(projectmembers__users__id = request.user.id).order_by('-created')
    # For users projects I use raw SQL query because it's complicated to compose correct orm-string for built-in group_concat function and left joins
    # This is lack of composition because it's not universal solutions if you want to change your database
    # Anyway, SQL query is protected from injection by using a parameters 
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
                group by pp.id
                order by created desc''', [request.user.id])
    user_info = User.objects.get(pk = request.user.id)
    context = {
        'title': "Projects",
        'header': "Projects",
        'all_projects': all_projects,
        'shared_projects': shared_projects,
        'my_projects': my_projects,
        'user': user_info,
        }

    return render(request, 'projects/index.html', context=context)

# Add new project 
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

# Edit existing project
@login_required(login_url="/signin")
def edit_project(request, id):
    if request.method == 'POST':
        # If presed 'Edit Project' button
        if request.POST.get("EditProject"):
            project_name = request.POST.get("project_name")
            project_description = request.POST.get("project_description")

            form = Project.objects.get(pk = id)
            if form is not None:
                form.name = project_name
                form.description = project_description
                form.save()

                return redirect("index")
        
        # If presed 'Remove Member' button
        elif request.POST.get("RemoveMember"):
            member_id = request.POST.get("select_members")
            ProjectMember.objects.filter(projects__id = id, users__id = member_id).delete()
            return redirect(request.META.get('HTTP_REFERER'))

        # If presed 'Invite' button
        elif request.POST.get("Invite"):
            email_member = request.POST.get("email_member")
            # try to get user with submitted email
            try:
                member = User.objects.get(email = email_member)
                # Check if user try to add themself as a member of project (prohibited!)
                if member.id == request.user.id:
                    messages.error(request, f"You are owner of this project. You cannot add yourself as member of the project.")
                else:
                    project = Project.objects.get(id = id)
                    project_memeber = ProjectMember.objects.filter(projects__id = id, users__id = member.id)
                    # Check if the user has already been added
                    if project_memeber:
                        messages.error(request, f"The user with email '{email_member}' has already been added as a member for the project '{project.name}'.")
                    else:
                        project_memeber = ProjectMember.objects.create(projects = project, users = member)
                        project_memeber.save()

                        # Refresh the same page
                        return redirect(request.META.get('HTTP_REFERER'))
            except:
                messages.error(request, f"The user with email '{email_member}' doesn't exists.")
    # Edit form is avalailable only for owner of the project and users who have been added into admin group or have high level access (supersusers)
    if Project.objects.filter(pk = id, owner = request.user) or request.user.groups.filter(name = 'admin').exists() or request.user.is_superuser:         
        project = Project.objects.get(pk = id)
        members = User.objects.filter(projectmember__projects__id = id).values_list('id', 'username')
        context = {
            'title': "Projects",
            'header': "Projects",
            'project': project,
            'members': members,
            }
        return render(request, 'projects/edit_project.html', context=context)
    else:
        return redirect("index")
        
# Remove project member
@login_required(login_url="/signin")
def remove_projectmember(request, id):
    if request.method == 'POST':
        if Project.objects.filter(pk = id, owner = request.user) or request.user.groups.filter(name = 'admin').exists() or request.user.is_superuser:   
            member_id = request.POST.get("select_members")
            ProjectMember.objects.filter(projects__id = id, users__id = member_id).delete()
            return redirect("index")
        else:
            messages.error(request, f"You cannot remove the project. You don't have permissions.")
            return redirect("index")
        
# Remove whole project
@login_required(login_url="/signin")
def remove_project(request, id):
    if Project.objects.filter(pk = id, owner = request.user) or request.user.groups.filter(name = 'admin').exists() or request.user.is_superuser:    
        Project.objects.filter(id = id).delete()
        return redirect("index")
    else:
        messages.error(request, f"You cannot remove the project. You don't have permissions.")
        return redirect("index")