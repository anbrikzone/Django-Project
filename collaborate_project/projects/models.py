from django.db import models
from django.contrib.auth.models import User, Group

class Project(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField()
    owner       = models.ManyToManyField(User)
    created     = models.DateTimeField()

# class ProjectMember(models.Model):
#     project  = models.ForeignKey(Project, on_delete = models.CASCADE)
#     users     = models.ForeignKey(User, default=models.SET_NULL, on_delete = models.CASCADE)


