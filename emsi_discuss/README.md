# EMSI_Discuss - Forum Académique

## 📋 Description du Projet

**EMSI_Discuss** est un forum de discussion académique conçu spécialement pour les étudiants de l'EMSI. Il permet aux étudiants de poser des questions, partager des connaissances et collaborer dans un environnement structuré.

### Objectif
Créer une plateforme de discussion académique avec un système de modération, de votes et de notifications pour favoriser l'apprentissage collaboratif.

---

## 🛠️ Technologie Utilisée

- **Backend** : Django 4.2 (Framework Python)
- **Base de données** : MySQL
- **Frontend** : Bootstrap 5
- **Serveur** : Django Development Server / Gunicorn (Production)

---

## 📦 Applications Django Créées

1. **accounts** - Gestion des utilisateurs et profils
2. **forum** - Catégories, sous-catégories, sujets et réponses
3. **votes** - Système de votes utile/pas utile
4. **moderation** - Signalements, masquage, verrouillage et bannissement
5. **notifications** - Système de notifications simples

---

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- MySQL Server 5.7+
- pip (gestionnaire de paquets Python)

### Étape 1 : Créer l'environnement virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Étape 2 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 3 : Configurer la base de données
```bash
# Créer la base de données MySQL
mysql -u root -p
```

Dans MySQL :
```sql
CREATE DATABASE emsi_discuss_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Étape 4 : Faire les migrations
```bash
python manage.py migrate
```

### Étape 5 : Créer un super utilisateur (admin)
```bash
python manage.py createsuperuser
```

### Étape 6 : Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

---

## 🎯 Lancer le Serveur

```bash
python manage.py runserver
```

L'application sera disponible sur : `http://127.0.0.1:8000/`

### Accès à l'Admin Django
- URL : `http://127.0.0.1:8000/admin/`
- Utiliser les identifiants du super utilisateur créé

---

## 📁 Structure du Projet

```
emsi_discuss/
├── emsi_discuss/          # Configuration du projet
│   ├── settings.py        # Paramètres Django
│   ├── urls.py           # Routes principales
│   ├── wsgi.py           # WSGI pour production
│   └── asgi.py           # ASGI pour WebSocket
├── accounts/             # Gestion des comptes
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── forum/                # Forum de discussion
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── votes/                # Système de votes
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── moderation/           # Modération du forum
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── notifications/        # Système de notifications
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── templates/            # Templates HTML
│   ├── base.html
│   └── home.html
├── static/               # Fichiers statiques
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔧 Commandes Utiles

### Création d'une nouvelle application
```bash
python manage.py startapp nom_app
```

### Créer les migrations
```bash
python manage.py makemigrations
```

### Appliquer les migrations
```bash
python manage.py migrate
```

### Lancer les tests
```bash
python manage.py test
```

### Lancer la console Django
```bash
python manage.py shell
```

### Vider la base de données
```bash
python manage.py flush
```

---

## 📝 Commandes d'Installation Rapide (Résumé)

```bash
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement (Windows)
venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer la base de données MySQL
# mysql -u root -p
# CREATE DATABASE emsi_discuss_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 5. Faire les migrations
python manage.py migrate

# 6. Créer un super utilisateur
python manage.py createsuperuser

# 7. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 8. Lancer le serveur
python manage.py runserver
```

---

## 🎨 Configuration Base de Données

Le fichier `settings.py` contient la configuration MySQL :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'emsi_discuss_db',
        'USER': 'root',
        'PASSWORD': '',  # À modifier avec votre mot de passe
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**À modifier selon votre configuration MySQL.**

---

## 📚 Prochaines Étapes

- [ ] Développer les templates pour chaque application
- [ ] Implémenter les vues détaillées
- [ ] Ajouter l'authentification et l'autorisation
- [ ] Configurer les permissions
- [ ] Ajouter les tests unitaires
- [ ] Mettre en place la pagination
- [ ] Ajouter les formulaires
- [ ] Implémenter le système de recherche
- [ ] Ajouter des validations côté serveur
- [ ] Déployer sur un serveur de production

---

## 👨‍💻 Auteur

Projet académique - EMSI_Discuss

---

## 📄 Licence

Ce projet est destiné à un usage éducatif.

---

## 📞 Support

Pour toute question ou assistance, veuillez contacter l'équipe pédagogique.

**Dernière mise à jour** : 22 Avril 2024
