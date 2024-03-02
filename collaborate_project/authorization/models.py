from django.db import models

class Users(models.Model):

    login       = models.CharField(max_length=64)
    password    = models.CharField(max_length=256)
    first_name  = models.CharField(max_length=128)
    last_name   = models.CharField(max_length=128)
    age         = models.SmallIntegerField()
    email       = models.EmailField()

