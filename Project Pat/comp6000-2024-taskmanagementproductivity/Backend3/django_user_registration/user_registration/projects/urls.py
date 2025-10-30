from django.urls import path
from .views import (create_project, delete_project, get_all_projects, get_project, update_project, get_project_members, add_project_member, get_all_users, user_profile_drop, get_user_by_username 
)

urlpatterns = [
    path('create-project/', create_project, name='create_project'),
    path('update-project/<int:pk>/', update_project, name='update_project'),
    path('delete-project/<int:pk>/', delete_project, name='delete_project'),
    path('get-all-projects/', get_all_projects, name='get_all_projects'),
    path('get-project/<int:pk>/', get_project, name='get_project'),

    # 👥 Member-related endpoints
    path('<int:project_id>/members/', get_project_members, name='project_members'),
    path('<int:project_id>/add-member/', add_project_member, name='add_project_member'),
    path('users/', get_all_users, name='get_all_users'),
    path('api/user-profile-drop/', user_profile_drop, name='user-profile-drop'),
    path('api/users/by-username/<str:username>/', get_user_by_username, name='get_user_by_username'),



]
