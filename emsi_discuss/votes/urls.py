"""
URLs pour l'application Votes
"""
from django.urls import path
from . import views

app_name = 'votes'

urlpatterns = [
    # Votes sur les topics
    path('topic/<int:topic_id>/vote/', views.vote_topic, name='vote_topic'),
    
    # Votes sur les réponses
    path('reply/<int:reply_id>/vote/', views.vote_reply, name='vote_reply'),
]
