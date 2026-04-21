"""
URLs pour l'application Votes
"""
from django.urls import path
from . import views

app_name = 'votes'

urlpatterns = [
    path('', views.votes_home, name='home'),
]
