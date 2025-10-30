from django.urls import path
from .views import create_task, delete_task, get_all_tasks, get_task, update_task, get_assigned_tasks
from . import views


urlpatterns = [
    path('create-task/', create_task, name='create_task'),
    path('update-task/<int:pk>/', update_task, name='update_task'),
    path('delete-task/<int:pk>/', delete_task, name='delete_task'),
    path('get-all-tasks/', get_all_tasks, name='get_all_tasks'),
    path('get-task/<int:pk>/', get_task, name='get_task'),
    path('get-assigned-tasks/', get_assigned_tasks, name='get_assigned_tasks'),
    path('api/activity-feed/', views.activity_feed, name='activity_feed'),

]