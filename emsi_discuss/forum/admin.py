"""
Administration pour l'application Forum
"""
from django.contrib import admin
from .models import Category, SubCategory, Tag, Topic, Reply


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin pour les catégories du forum
    """
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """
    Admin pour les sous-catégories du forum
    """
    list_display = ('name', 'category', 'slug', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin pour les tags
    """
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """
    Admin pour les sujets du forum
    """
    list_display = ('title', 'get_category', 'subcategory', 'author', 'is_solved', 'is_locked', 'is_pinned', 'created_at')
    list_filter = ('is_solved', 'is_locked', 'is_pinned', 'created_at', 'subcategory__category')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at', 'views_count', 'get_author_display')
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Informations', {
            'fields': ('author', 'subcategory', 'title', 'content')
        }),
        ('Tags et Anonymat', {
            'fields': ('tags', 'is_anonymous')
        }),
        ('État du Sujet', {
            'fields': ('is_solved', 'is_locked', 'is_pinned')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at', 'views_count', 'get_author_display'),
            'classes': ('collapse',)
        }),
    )

    def get_category(self, obj):
        """Affiche la catégorie parente"""
        return obj.get_category()
    get_category.short_description = 'Catégorie'


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    """
    Admin pour les réponses du forum
    """
    list_display = ('id', 'topic', 'author', 'is_best_answer', 'is_hidden', 'created_at')
    list_filter = ('is_best_answer', 'is_hidden', 'created_at', 'topic__subcategory__category')
    search_fields = ('content', 'author__username', 'topic__title')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations', {
            'fields': ('author', 'topic', 'content', 'quoted_reply')
        }),
        ('État', {
            'fields': ('is_best_answer', 'is_hidden')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    raw_id_fields = ('topic', 'quoted_reply')
