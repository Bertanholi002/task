from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks', views.tasks, name='tasks'),
    path('tasks/<task_id>/', views.task, name='task'),
    path('new_task', views.new_task, name='new_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
]
