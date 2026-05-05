"""
Formulaires pour l'application Forum
"""
from django import forms
from .models import Topic, Tag, Category


class TopicCreateForm(forms.ModelForm):
    """
    Formulaire pour créer un nouveau sujet/discussion
    Permet à l'utilisateur de saisir librement la sous-catégorie et les tags
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label='Catégorie *',
        help_text='Sélectionnez la catégorie principale'
    )
    
    subcategory_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Python, Django, Machine Learning...',
        }),
        label='Sous-catégorie *',
        help_text='Entrez le nom de la sous-catégorie (sera créée automatiquement si elle n\'existe pas)'
    )
    
    tag_names = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': '#python #django #bug #question',
        }),
        label='Tags',
        help_text='Entrez les tags séparés par un espace, chacun commençant par #. Exemple: #python #django #bug'
    )

    class Meta:
        model = Topic
        fields = ('title', 'content', 'is_anonymous')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de votre sujet',
                'maxlength': '200',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Détail de votre question ou sujet...',
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'title': 'Titre *',
            'content': 'Contenu *',
            'is_anonymous': 'Poster de manière anonyme',
        }
        help_texts = {
            'title': 'Soyez descriptif et clair',
            'content': 'Fournissez autant de détails que possible pour obtenir de bonnes réponses',
        }

    def clean_title(self):
        """Valide le titre"""
        title = self.cleaned_data.get('title')
        if title and len(title) < 5:
            raise forms.ValidationError('Le titre doit contenir au moins 5 caractères.')
        return title

    def clean_content(self):
        """Valide le contenu"""
        content = self.cleaned_data.get('content')
        if content and len(content) < 20:
            raise forms.ValidationError('Le contenu doit contenir au moins 20 caractères.')
        return content
    
    def clean_subcategory_name(self):
        """Valide la sous-catégorie"""
        subcategory_name = self.cleaned_data.get('subcategory_name')
        if subcategory_name and len(subcategory_name) < 2:
            raise forms.ValidationError('La sous-catégorie doit contenir au moins 2 caractères.')
        return subcategory_name


class TopicUpdateForm(forms.ModelForm):
    """
    Formulaire pour modifier un sujet existant
    Permet de modifier le titre, contenu et tags
    Catégorie et sous-catégorie ne peuvent pas être modifiées
    """
    tag_names = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': '#python #django #bug #question',
        }),
        label='Tags',
        help_text='Entrez les tags séparés par un espace, chacun commençant par #. Exemple: #python #django #bug'
    )

    class Meta:
        model = Topic
        fields = ('title', 'content', 'is_anonymous')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de votre sujet',
                'maxlength': '200',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Détail de votre question ou sujet...',
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'title': 'Titre *',
            'content': 'Contenu *',
            'is_anonymous': 'Poster de manière anonyme',
        }

    def clean_title(self):
        """Valide le titre"""
        title = self.cleaned_data.get('title')
        if title and len(title) < 5:
            raise forms.ValidationError('Le titre doit contenir au moins 5 caractères.')
        return title

    def clean_content(self):
        """Valide le contenu"""
        content = self.cleaned_data.get('content')
        if content and len(content) < 20:
            raise forms.ValidationError('Le contenu doit contenir au moins 20 caractères.')
        return content
