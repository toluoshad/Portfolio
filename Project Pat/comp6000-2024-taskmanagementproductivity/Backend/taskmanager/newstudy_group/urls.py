from django.urls import path
from .views import create_study_group, add_member_to_group, create_task, get_tasks_for_group

urlpatterns = [
    path('api/groups', create_study_group, name='create_study_group'),
    path('api/groups/<int:group_id>/add-member', add_member_to_group, name='add_member_to_group'),
    path('api/tasks', create_task, name='create_task'),
    path('api/groups/<int:group_id>/tasks', get_tasks_for_group, name='get_tasks_for_group'),
]