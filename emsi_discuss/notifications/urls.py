"""
URLs pour l'application Notifications
"""
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('read/<int:notification_id>/', views.mark_notification_read, name='mark_read'),
    path('read-all/', views.mark_all_notifications_read, name='mark_all_read'),
]
