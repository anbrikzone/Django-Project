from django.db import models
from django.forms import ModelForm

# class Roles(models.Model):
#     USER    = "User"
#     OWNER   = "Owner"
#     ADMIN   = "Admin"
#     ROLES   = [
#         (USER, "User"),
#         (OWNER, "Owner"),
#         (ADMIN, "Admin")
#     ]
#     type    = models.CharField(max_length=5, choices=ROLES, default=USER)

# class Users(models.Model):
#     login       = models.CharField(max_length=64)
#     password    = models.CharField(max_length=256)
#     first_name  = models.CharField(max_length=128)
#     last_name   = models.CharField(max_length=128)
#     age         = models.SmallIntegerField()
#     email       = models.EmailField()
#     role       = models.ForeignKey(Roles, on_delete=models.CASCADE)