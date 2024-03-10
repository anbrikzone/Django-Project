from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_project/', views.add_project, name='add_project'),
    path('edit_project/<int:id>', views.edit_project, name='edit_project'),
    path('remove_project/<int:id>', views.remove_project, name='remove_project'),
    path('remove_projectmember/<int:id>', views.remove_projectmember, name='remove_projectmember'),
]