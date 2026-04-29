"""
Administration pour l'application Forum
"""
from django.contrib import admin
from .models import Category, SubCategory, Topic, Reply, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'subcategory', 'is_locked', 'is_pinned', 'created_at')
    list_filter = ('is_locked', 'is_pinned', 'is_solved', 'is_anonymous', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('tags',)

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'topic', 'is_best_answer', 'is_hidden', 'created_at')
    list_filter = ('is_best_answer', 'is_hidden', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('created_at', 'updated_at')
