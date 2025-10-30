from django.urls import path
from .views import register_user, delete_user, login_user, logout_user, password_reset_request, password_reset_confirm, get_all_users, user_profile, user_profile_drop, update_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('delete-user/', delete_user, name='delete_user'),
    path('profile/', user_profile, name='profile'),
    path('logout/', logout_user, name='logout'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-confirm/', password_reset_confirm, name='password_reset_confirm'),
    path('users/', get_all_users, name='get_all_users'),
    path('user-profile-drop/', user_profile_drop, name='user_profile_drop'),  # ✅ This is correct
    path('update-user/', update_user, name='update_user')
]