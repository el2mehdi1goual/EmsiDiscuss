"""
URLs pour l'application Notifications
"""
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notifications_home, name='home'),
]
