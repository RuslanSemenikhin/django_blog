from django.urls import path, re_path
from .views import (register, log_in,
                    log_out, get_user_info)

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('profile/<int:pk>/', get_user_info, name='profile'),
]

