"""
Modèles pour l'application Forum
Structure : Category > SubCategory > Topic
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """
    Catégorie principale du forum
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Génère automatiquement le slug"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    """
    Sous-catégorie du forum (enfant d'une Category)
    Créée automatiquement par les utilisateurs lors de la création d'un sujet
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sous-catégorie'
        verbose_name_plural = 'Sous-catégories'
        ordering = ['name']
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category.name} > {self.name}"

    def save(self, *args, **kwargs):
        """Génère automatiquement le slug"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """
    Tag/Étiquette pour catégoriser les sujets
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Génère automatiquement le slug"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Topic(models.Model):
    """
    Sujet/Discussion du forum
    """
    # Auteur et localisation
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='topics')
    
    # Contenu
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='topics', blank=True)
    
    # Anonymat
    is_anonymous = models.BooleanField(default=False, help_text="Poster de façon anonyme")
    
    # État du sujet
    is_solved = models.BooleanField(default=False, help_text="Sujet résolu")
    is_locked = models.BooleanField(default=False, help_text="Sujet verrouillé (pas de réponses)")
    is_pinned = models.BooleanField(default=False, help_text="Sujet épinglé en haut")
    is_hidden = models.BooleanField(default=False, help_text="Sujet masqué par modération")
    hidden_reason = models.CharField(max_length=255, blank=True, help_text="Raison du masquage")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0, help_text="Nombre de vues")

    class Meta:
        verbose_name = 'Sujet'
        verbose_name_plural = 'Sujets'
        ordering = ['-is_pinned', '-created_at']  # Épinglés d'abord, puis récents

    def __str__(self):
        return self.title

    def get_category(self):
        """Retourne la catégorie parente via la subcategory"""
        return self.subcategory.category

    def get_author_display(self):
        """Retourne le nom de l'auteur ou 'Anonyme'"""
        if self.is_anonymous:
            return 'Anonyme'
        return self.author.get_full_name() or self.author.username

    def increment_views(self):
        """Incrémente le compteur de vues"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Reply(models.Model):
    """
    Réponse à un sujet du forum
    """
    # Auteur et localisation
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='replies')
    
    # Contenu
    content = models.TextField()
    quoted_reply = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='quotes'
    )
    
    # État
    is_best_answer = models.BooleanField(default=False, help_text="Meilleure réponse")
    is_hidden = models.BooleanField(default=False, help_text="Réponse masquée")
    hidden_reason = models.CharField(max_length=255, blank=True, help_text="Raison du masquage")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Réponse'
        verbose_name_plural = 'Réponses'
        ordering = ['is_best_answer', 'created_at']

    def __str__(self):
        return f"Réponse de {self.author} sur {self.topic.title}"

    def get_author_display(self):
        """Retourne le nom de l'auteur"""
        return self.author.get_full_name() or self.author.username
