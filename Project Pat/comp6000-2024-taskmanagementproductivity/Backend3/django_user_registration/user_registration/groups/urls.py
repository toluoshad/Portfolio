from django.urls import path
from . import views

urlpatterns = [
    path('api/groups/all/', views.get_all_groups, name='get_all_groups'),
    path('api/groups/create/', views.create_group, name='create_group'),
    path('api/groups/', views.get_user_groups, name='get_user_groups'),
    path('api/groups/<int:group_id>/update/', views.update_group, name='update_group'),
    path('api/groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),  # Changed here
    path('api/groups/<int:group_id>/add-member/', views.add_member, name='add_member'),
    path('api/users/by-username/<str:username>/', views.get_user_by_username, name='get_user_by_username'),
    path('api/groups/<int:group_id>/leave/', views.remove_self, name='remove_self'),
    path('api/groups/<int:group_id>/remove-member/', views.remove_member, name='remove_member'),
    path('api/groups/<int:group_id>/transfer-admin/', views.transfer_admin, name='transfer_admin'),
    
    


]
