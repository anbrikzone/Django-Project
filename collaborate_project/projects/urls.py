from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_project/', views.add_project, name='add_project'),
    path('edit_project/', views.edit_project, name='edit_project'),
]