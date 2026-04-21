# 🎯 Guide Visuel - Architecture EMSI_Discuss

## 📊 Flux de Requête HTTP

```
Utilisateur accède à http://127.0.0.1:8000/
    ↓
emsi_discuss/urls.py → path('', views.home, name='home')
    ↓
emsi_discuss/views.py → home(request) retourne templates/home.html
    ↓
templates/home.html (hérité de templates/base.html)
    ↓
static/css/style.css + static/js/main.js
    ↓
Page affichée dans le navigateur avec Bootstrap 5
```

---

## 🗂️ Arborescence des Applications

### 1️⃣ Application: ACCOUNTS (Gestion des Comptes)

```
accounts/
├── models.py
│   └── UserProfile (profil utilisateur)
├── views.py
│   └── accounts_home()
├── urls.py
│   └── path('', accounts_home, name='home')
├── admin.py
│   └── UserProfileAdmin
└── migrations/
```

**Accès:** http://127.0.0.1:8000/accounts/

---

### 2️⃣ Application: FORUM (Forum de Discussion)

```
forum/
├── models.py
│   ├── Category
│   ├── SubCategory
│   ├── Topic
│   └── Reply
├── views.py
│   └── forum_home()
├── urls.py
│   └── path('', forum_home, name='home')
├── admin.py
│   ├── CategoryAdmin
│   ├── SubCategoryAdmin
│   ├── TopicAdmin
│   └── ReplyAdmin
└── migrations/
```

**Accès:** http://127.0.0.1:8000/forum/

---

### 3️⃣ Application: VOTES (Système de Votes)

```
votes/
├── models.py
│   └── Vote (lié à Reply)
├── views.py
│   └── votes_home()
├── urls.py
│   └── path('', votes_home, name='home')
├── admin.py
│   └── VoteAdmin
└── migrations/
```

**Accès:** http://127.0.0.1:8000/votes/

---

### 4️⃣ Application: MODERATION (Modération)

```
moderation/
├── models.py
│   ├── Report (signalements)
│   └── Ban (bannissements)
├── views.py
│   └── moderation_home()
├── urls.py
│   └── path('', moderation_home, name='home')
├── admin.py
│   ├── ReportAdmin
│   └── BanAdmin
└── migrations/
```

**Accès:** http://127.0.0.1:8000/moderation/

---

### 5️⃣ Application: NOTIFICATIONS (Notifications)

```
notifications/
├── models.py
│   └── Notification
├── views.py
│   └── notifications_home()
├── urls.py
│   └── path('', notifications_home, name='home')
├── admin.py
│   └── NotificationAdmin
└── migrations/
```

**Accès:** http://127.0.0.1:8000/notifications/

---

## 🔗 Relations entre les Modèles

```
                    ┌─────────────┐
                    │ User (auth) │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────────┐  ┌───────────┐      ┌────────────────┐
    │UserProfile │  │  Topic    │      │  Notification  │
    └────────────┘  │(1 author) │      └────────────────┘
                    └──────┬────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────┐        ┌────────┐         ┌────────┐
    │ Reply  │        │ Report │         │  Vote  │
    └────────┘        └────────┘         └────────┘
```

---

## 📋 Configuration Django (settings.py)

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Nos applications
    'accounts',      # ✓ Créée
    'forum',         # ✓ Créée
    'votes',         # ✓ Créée
    'moderation',    # ✓ Créée
    'notifications', # ✓ Créée
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'emsi_discuss_db',  # ✓ À créer
        'USER': 'root',
        'PASSWORD': '',  # À adapter
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],  # ✓ Créé
        ...
    }
]
```

---

## 🌐 Routes Disponibles

| URL | Vue | Description |
|-----|-----|-------------|
| `/` | home | Page d'accueil |
| `/admin/` | Admin | Panneau d'administration |
| `/accounts/` | accounts_home | Gestion des comptes |
| `/forum/` | forum_home | Forum de discussion |
| `/votes/` | votes_home | Système de votes |
| `/moderation/` | moderation_home | Modération |
| `/notifications/` | notifications_home | Notifications |

---

## 📝 Fichiers Templates

```
templates/
│
├── base.html                    ← Template de base
│   ├── <html>
│   ├── <head>
│   │   ├── Bootstrap 5 CDN
│   │   └── static/css/style.css
│   ├── <body>
│   │   ├── Navigation navbar
│   │   ├── {% block content %}
│   │   └── Footer
│   └── {% block extra_js %}
│
└── home.html                    ← Page d'accueil
    ├── {% extends 'base.html' %}
    ├── Jumbotron (titre + description)
    ├── Cartes des modules
    ├── Section "À propos"
    └── État du développement
```

---

## 🎨 Fichiers Statiques

### CSS (style.css)
```css
/* Variables */
:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    ...
}

/* Sections */
- Body & General
- Navigation
- Jumbotron
- Cards
- Badges
- Alerts
- Buttons
- Lists
- Footer
- Responsive
- Animations
```

### JavaScript (main.js)
```javascript
// Attendre le DOM
document.addEventListener('DOMContentLoaded', ...)

// Fermer les alertes
// Animations au défilement
// Notifications
// Requêtes AJAX
```

---

## 🔄 Cycle de Développement

### Phase 1 : ✅ Initialisation (COMPLÉTÉE)
- Structure du projet ✓
- Applications ✓
- Modèles ✓
- Configuration ✓

### Phase 2 : À venir - Authentification
- Formulaires de connexion/inscription
- Vue d'authentification
- Permissions et groupes

### Phase 3 : À venir - Fonctionnalités
- CRUD complets
- Recherche et filtrage
- Pagination

### Phase 4 : À venir - API
- REST API
- Authentification API
- Tests

### Phase 5 : À venir - Production
- Déploiement
- SSL/HTTPS
- Base de données distante

---

## 🧪 Tests et Vérification

```bash
# 1. Vérifier l'installation
python manage.py check

# 2. Vérifier les migrations
python manage.py migrate --plan

# 3. Créer des données de test
python manage.py shell

# 4. Lancer les tests
python manage.py test

# 5. Couvrir les tests
coverage run --source='.' manage.py test
```

---

## 📊 Matrice des Dépendances

```
Settings ├─ MySQL Database
         ├─ Applications (5)
         ├─ Templates
         ├─ Static Files
         └─ Middleware

Applications ├─ Models
             ├─ Views
             ├─ URLs
             ├─ Admin
             └─ Migrations

Database ├─ Category
         ├─ SubCategory
         ├─ Topic
         ├─ Reply
         ├─ UserProfile
         ├─ Vote
         ├─ Report
         ├─ Ban
         └─ Notification
```

---

## 🎯 Points de Vérification Avant Présentation

### ✅ Avant la Séance

1. **Base de Données**
   - [ ] MySQL installé et en cours d'exécution
   - [ ] Base de données `emsi_discuss_db` créée
   - [ ] Migrations appliquées

2. **Django**
   - [ ] Environnement virtuel créé
   - [ ] Dépendances installées
   - [ ] Admin Django accessible
   - [ ] Super utilisateur créé

3. **Application**
   - [ ] Page d'accueil affichée correctement
   - [ ] Navigation fonctionnelle
   - [ ] Styles Bootstrap appliqués
   - [ ] Admin accessible (login)

4. **Fichiers**
   - [ ] Tous les modèles visibles en admin
   - [ ] Templates affichés correctement
   - [ ] CSS et JS chargés

---

## 💡 Commandes Essentielles Rapides

```bash
# Setup complet
python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt

# Migrations
python manage.py migrate

# Admin
python manage.py createsuperuser

# Lancer
python manage.py runserver

# Accéder
# http://127.0.0.1:8000/       (Accueil)
# http://127.0.0.1:8000/admin/ (Admin)
```

---

## 📚 Références Rapides

- [Django Documentation](https://docs.djangoproject.com/) - Framework
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/) - Styles
- [MySQL Documentation](https://dev.mysql.com/doc/) - Base de données
- [Python](https://docs.python.org/3/) - Langage

---

**Projet: EMSI_Discuss**  
**Statut:** ✅ Initialisé et Prêt  
**Version:** 1.0  
**Date:** 22 Avril 2024
