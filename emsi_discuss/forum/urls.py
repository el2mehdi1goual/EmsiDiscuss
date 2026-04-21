"""
URLs pour l'application Forum
"""
from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_home, name='home'),
]
