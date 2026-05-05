"""
Formulaires pour l'application Forum
"""
from django import forms
from .models import Topic, Tag, Category, SubCategory, Reply


class TopicCreateForm(forms.ModelForm):
    """
    Formulaire pour créer un nouveau sujet/discussion
    Permet à l'utilisateur de sélectionner une sous-catégorie existante ou d'en créer une nouvelle
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_category',
        }),
        label='Catégorie *',
        help_text='Sélectionnez la catégorie principale'
    )
    
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.none(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_subcategory',
        }),
        label='Sous-catégorie existante',
        help_text='Sélectionnez une sous-catégorie existante'
    )
    
    new_subcategory_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Python, Django, Machine Learning...',
            'id': 'id_new_subcategory',
        }),
        label='Ou créer une nouvelle sous-catégorie',
        help_text='Laissez vide si vous choisissez une existante'
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

    def __init__(self, *args, **kwargs):
        """Initialise le formulaire et filtre les sous-catégories selon la catégorie sélectionnée"""
        super().__init__(*args, **kwargs)
        # Par défaut, pas de sous-catégories (elles seront chargées via JavaScript)
        self.fields['subcategory'].queryset = SubCategory.objects.none()

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
    
    def clean(self):
        """Valide que soit une sous-catégorie existante est sélectionnée, soit une nouvelle est créée"""
        cleaned_data = super().clean()
        subcategory = cleaned_data.get('subcategory')
        new_subcategory_name = cleaned_data.get('new_subcategory_name', '').strip()
        
        # Vérifier qu'une des deux options est fournie
        if not subcategory and not new_subcategory_name:
            raise forms.ValidationError(
                'Veuillez sélectionner une sous-catégorie existante ou en créer une nouvelle.'
            )
        
        # Vérifier la longueur de la nouvelle sous-catégorie si fournie
        if new_subcategory_name and len(new_subcategory_name) < 2:
            raise forms.ValidationError(
                'La nouvelle sous-catégorie doit contenir au moins 2 caractères.'
            )
        
        return cleaned_data


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


class ReplyForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une réponse
    """
    class Meta:
        model = Reply
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Entrez votre réponse...',
            }),
        }
        labels = {
            'content': 'Réponse *',
        }

    def clean_content(self):
        """Valide le contenu"""
        content = self.cleaned_data.get('content')
        if content and len(content) < 5:
            raise forms.ValidationError('La réponse doit contenir au moins 5 caractères.')
        return content
