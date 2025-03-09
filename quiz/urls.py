from django.urls import path
from .views import *

app_name = 'quiz'

urlpatterns = [
    path('', quiz_view, name='quiz_home'),
    path('submit-answer/', submit_answer, name='submit_answer'),
    path('register/', register_user, name='register_user'),
    path('logout/', logout_user, name='logout_user'),  # مسیر جدید برای خروج
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('manage-users/', manage_users, name='manage_users'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
]