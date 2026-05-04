"""
Formulaires pour l'application Accounts
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegisterForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé
    Crée un nouvel User avec email, username, password et infos de profil
    """
    email = forms.EmailField(
        required=True,
        label='Adresse email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com',
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom d\'utilisateur',
        })
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label='Prénom',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre prénom',
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label='Nom',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom',
        })
    )
    filiere = forms.CharField(
        max_length=100,
        required=False,
        label='Filière',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Informatique, Génie Logiciel',
        })
    )
    promotion = forms.CharField(
        max_length=50,
        required=False,
        label='Promotion/Année',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: 2024, L3, Master 1',
        })
    )
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre mot de passe',
        })
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        """Vérifie que l'email n'existe pas déjà"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Cet email est déjà utilisé.')
        return email

    def save(self, commit=True):
        """
        Crée l'utilisateur et remplit les informations de son profil
        """
        user = super().save(commit=commit)
        
        if commit:
            # Mettre à jour le profil après la création du user
            profile = user.profile
            profile.filiere = self.cleaned_data.get('filiere', '')
            profile.promotion = self.cleaned_data.get('promotion', '')
            profile.save()
        
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Formulaire pour modifier les informations utilisateur (User)
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com',
        })
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label='Prénom',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre prénom',
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label='Nom',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom',
        })
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        """Vérifie l'unicité de l'email"""
        email = self.cleaned_data.get('email')
        # Exclure l'utilisateur actuel
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Cet email est déjà utilisé.')
        return email


class ProfileUpdateForm(forms.ModelForm):
    """
    Formulaire pour modifier le profil utilisateur (Profile)
    """
    avatar = forms.ImageField(
        required=False,
        label='Avatar',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
        })
    )
    bio = forms.CharField(
        max_length=500,
        required=False,
        label='Biographie',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Parlez un peu de vous...',
        })
    )
    signature = forms.CharField(
        max_length=255,
        required=False,
        label='Signature',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre signature',
        })
    )
    filiere = forms.CharField(
        max_length=100,
        required=False,
        label='Filière',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Informatique',
        })
    )
    promotion = forms.CharField(
        max_length=50,
        required=False,
        label='Promotion/Année',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: 2024',
        })
    )

    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'signature', 'filiere', 'promotion')
