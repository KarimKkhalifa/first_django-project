from django.urls import path, include
from user.views import *

urlpatterns = [
    path('user/', include([
        path('user_profile/', get_user_profile, name='user_profile'),
        path('user_profile/<int:pk>/delete', delete_user_account, name='delete_user'),
        path('register/', register, name='register'),
        path('login/', user_login, name='login'),
        path('logout/', user_logout, name='logout'),
    ])),
]
