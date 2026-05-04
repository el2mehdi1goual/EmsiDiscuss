"""
URLs pour l'application Accounts
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentification
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Profil
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
