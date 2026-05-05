"""
URLs pour l'application Forum
"""
from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    # Page d'accueil du forum
    path('', views.forum_home, name='home'),
    
    # Topics - Liste et Détail
    path('topics/', views.topic_list, name='topic_list'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    
    # Topics - CRUD
    path('topic/create/', views.topic_create, name='topic_create'),
    path('topic/<int:topic_id>/edit/', views.topic_update, name='topic_update'),
    path('topic/<int:topic_id>/delete/', views.topic_delete, name='topic_delete'),
]
