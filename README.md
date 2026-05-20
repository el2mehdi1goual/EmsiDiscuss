# 🎓 EMSI_Discuss - Forum Académique

Bienvenue ! Ce dossier contient le projet Django complet pour **EMSI_Discuss**, un forum de discussion académique pour les étudiants EMSI.

## 📖 Documentation

### Architecture et Diagrammes
- **[Diagrammes de Classes UML (PlantUML)](CLASS_DIAGRAM.md)** - Diagrammes complets de toutes les classes avec descriptions détaillées des méthodes et relations

### Processus et Workflows
- **[Flux "Meilleure Réponse"](BEST_ANSWER_WORKFLOW.md)** - Détail complet du processus quand un utilisateur clique sur le bouton "Meilleure réponse" (permissions, modifications BD, notifications, réputation, etc.)
- **[is_solved vs is_locked](IS_SOLVED_VS_IS_LOCKED.md)** - Analyse des deux approches: faut-il verrouiller automatiquement un sujet résolu? Recommandations et bonnes pratiques

## 🏗️ Structure du Projet

```
EmsiDiscuss/
├── README.md                          # Cette documentation
├── CLASS_DIAGRAM.md                   # Diagrammes UML PlantUML détaillés
├── requirements.txt                   # Dépendances Python
├── db.sqlite3                         # Base de données (développement)
├── manage.py                          # Management CLI Django
│
└── emsi_discuss/                      # Répertoire principal du projet
    ├── settings.py                    # Configuration Django
    ├── urls.py                        # Routes principales
    ├── views.py                       # Vues principales
    ├── wsgi.py                        # Configuration WSGI
    ├── asgi.py                        # Configuration ASGI
    │
    ├── accounts/                      # App: Gestion des utilisateurs
    │   ├── models.py                  # Modèle Profile
    │   ├── views.py                   # Vues auth (login, register, profil)
    │   ├── forms.py                   # Formulaires enregistrement/édition
    │   ├── urls.py                    # Routes accounts
    │   └── templates/accounts/        # Templates HTML
    │
    ├── forum/                         # App: Forum principal
    │   ├── models.py                  # Modèles (Category, SubCategory, Topic, Reply, Tag)
    │   ├── views.py                   # Vues forum (list, detail, create, update)
    │   ├── forms.py                   # Formulaires (TopicCreateForm, TopicUpdateForm)
    │   ├── urls.py                    # Routes forum
    │   ├── migrations/                # Migrations BD
    │   └── templates/forum/           # Templates HTML
    │
    ├── moderation/                    # App: Modération et signalements
    │   ├── models.py                  # Modèle Report (GenericForeignKey)
    │   ├── views.py                   # Vues modération
    │   ├── forms.py                   # Formulaires signalement
    │   ├── urls.py                    # Routes modération
    │   ├── migrations/                # Migrations BD
    │   └── templates/moderation/      # Templates HTML
    │
    ├── notifications/                 # App: Système de notifications
    │   ├── models.py                  # Modèle Notification
    │   ├── views.py                   # Vues notifications
    │   ├── urls.py                    # Routes notifications
    │   ├── migrations/                # Migrations BD
    │   └── templates/notifications/   # Templates HTML
    │
    ├── votes/                         # App: Système de votes
    │   ├── models.py                  # Modèles (TopicVote, ReplyVote)
    │   ├── views.py                   # Vues votes (AJAX)
    │   ├── urls.py                    # Routes votes
    │   ├── migrations/                # Migrations BD
    │   └── api.py                     # API endpoints JSON
    │
    ├── static/                        # Fichiers statiques
    │   ├── css/
    │   │   └── style.css
    │   ├── js/
    │   │   └── main.js
    │   └── images/
    │
    ├── templates/                     # Templates principaux
    │   ├── base.html                  # Template de base
    │   └── home.html                  # Page d'accueil
    │
    ├── logs/                          # Fichiers de log
    └── media/                         # Fichiers uploadés
        └── avatars/                   # Avatars utilisateurs
```

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.8+
- pip ou poetry
- Virtual Environment

### Étapes d'installation

```bash
# 1. Créer et activer l'environnement virtuel
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # Linux/Mac

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Appliquer les migrations
python manage.py migrate

# 4. Créer un superutilisateur
python manage.py createsuperuser

# 5. Démarrer le serveur de développement
python manage.py runserver
```

L'application sera accessible à `http://localhost:8000`

## 📊 Diagramme Global du Projet

Pour une documentation complète sur l'architecture, les modèles et les relations entre classes, consultez [CLASS_DIAGRAM.md](CLASS_DIAGRAM.md).

### Applications principales

| App | Rôle | Modèles principaux |
|-----|------|-------------------|
| **Forum** | Gestion des sujets et réponses | Category, SubCategory, Topic, Reply, Tag |
| **Accounts** | Gestion des utilisateurs | Profile (extends Django User) |
| **Votes** | Système de votes | TopicVote, ReplyVote |
| **Moderation** | Signalements et modération | Report |
| **Notifications** | Notifications utilisateurs | Notification |

## 🔑 Concepts Clés

### Hiérarchie des catégories
```
Category (Catégories principales)
  └── SubCategory (Sous-catégories)
      └── Topic (Sujets de discussion)
          └── Reply (Réponses)
```

### Système de rôles
- **User**: Utilisateur normal
- **Moderator**: Peut examiner et résoudre les signalements
- **Admin**: Accès complet

### Gestion du contenu masqué
- Topics et Replies peuvent être masqués par modération
- Les utilisateurs normaux ne voient pas le contenu masqué
- Les modérateurs/admins voient le contenu avec raison de masquage

### Système de votes
- Chaque user ne peut voter qu'une fois par Topic/Reply
- Valeurs: 1 (Utile) ou -1 (Pas utile)
- Impacte la réputation de l'auteur

## 🛠️ Commandes Django Utiles

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Shell Django (pour tester)
python manage.py shell

# Créer un superutilisateur supplémentaire
python manage.py createsuperuser

# Vider la base de données
python manage.py flush

# Recréer la BD à zéro
python manage.py flush --no-input
python manage.py migrate
```

## 🌐 Routes principales

### Forum
- `/forum/` - Accueil forum
- `/forum/topics/` - Liste des sujets
- `/forum/topic/<id>/` - Détail d'un sujet
- `/forum/create/` - Créer un sujet

### Accounts
- `/accounts/register/` - Inscription
- `/accounts/login/` - Connexion
- `/accounts/logout/` - Déconnexion
- `/accounts/profile/` - Profil personnel
- `/accounts/profile/<username>/` - Profil d'un autre utilisateur
- `/accounts/edit-profile/` - Éditer profil

### Moderation
- `/moderation/reports/` - Liste des signalements
- `/moderation/report/<id>/` - Détail d'un signalement

### Notifications
- `/notifications/` - Vue des notifications

## 📝 Conventions de Code

- **Nommage**: snake_case pour les variables, PascalCase pour les classes
- **Docstrings**: Classes et méthodes doivent avoir des docstrings
- **Commentaires**: Expliker le "pourquoi", pas le "quoi"
- **Formatage**: PEP 8 avec max 120 caractères par ligne

## 🤝 Contribution

Pour contribuer au projet:
1. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
2. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
3. Push la branche (`git push origin feature/AmazingFeature`)
4. Ouvrir une Pull Request

## 📄 Licence

Ce projet est un projet académique EMSI.

## ✨ Crédits

Développé par l'équipe EMSI_Discuss
