"""
Administration pour l'application Forum
"""
from django.contrib import admin
from .models import Category, SubCategory, Topic, Reply


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Administrateur pour le modèle Category
    """
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """
    Administrateur pour le modèle SubCategory
    """
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """
    Administrateur pour le modèle Topic
    """
    list_display = ('title', 'author', 'subcategory', 'views_count', 'is_locked', 'created_at')
    list_filter = ('is_locked', 'is_pinned', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at', 'views_count')


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    """
    Administrateur pour le modèle Reply
    """
    list_display = ('author', 'topic', 'is_best_answer', 'created_at')
    list_filter = ('is_best_answer', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('created_at', 'updated_at')
