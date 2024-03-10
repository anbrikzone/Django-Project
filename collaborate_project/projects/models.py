from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone

class Project(models.Model):
    name        = models.CharField(max_length = 255)
    description = models.TextField()
    owner       = models.ForeignKey(User, on_delete = models.CASCADE)
    created     = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    projects  = models.ForeignKey(Project, related_name="projectmembers", on_delete = models.CASCADE)
    users     = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name


