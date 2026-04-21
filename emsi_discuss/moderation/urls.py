"""
URLs pour l'application Moderation
"""
from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('', views.moderation_home, name='home'),
]
