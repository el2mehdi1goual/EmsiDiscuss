"""
URLs pour l'application Moderation
"""
from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    # Signalements
    path('report/<str:content_type_name>/<int:object_id>/', views.report_content, name='report_content'),
    path('reports/', views.reports_list, name='reports_list'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
]
