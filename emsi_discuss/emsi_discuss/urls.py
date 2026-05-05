"""
URL configuration for emsi_discuss project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from . import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app import views
    2. Add a URL to urlpatterns:  path('', views.Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from forum import views as forum_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Page d'accueil - Affiche directement la liste des topics
    path('', forum_views.topic_list, name='home'),
    
    
    # Applications
    path('accounts/', include('accounts.urls')),
    path('forum/', include('forum.urls')),
    path('votes/', include('votes.urls')),
    path('moderation/', include('moderation.urls')),
    path('notifications/', include('notifications.urls')),
]

# Servir les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
