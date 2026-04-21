# 🎓 EMSI_Discuss - Forum Académique

Bienvenue ! Ce dossier contient le projet Django complet pour **EMSI_Discuss**, un forum de discussion académique pour les étudiants EMSI.

## 📂 Structure du Projet

```
EmsiDiscuss/
├── emsi_discuss/              # Projet Django complet
│   ├── emsi_discuss/          # Configuration du projet
│   ├── accounts/              # Gestion des comptes
│   ├── forum/                 # Forum de discussion
│   ├── votes/                 # Système de votes
│   ├── moderation/            # Modération
│   ├── notifications/         # Notifications
│   ├── templates/             # Templates HTML
│   ├── static/                # Fichiers CSS, JS, images
│   ├── manage.py              # Gestionnaire Django
│   ├── requirements.txt        # Dépendances Python
│   └── README.md              # Documentation du projet
├── COMMANDES_TERMINAL.md      # Guide des commandes
└── README.md                  # Ce fichier
```

## 🚀 Démarrage Rapide

### 1. Naviguez dans le dossier du projet
```bash
cd emsi_discuss
```

### 2. Créez et activez l'environnement virtuel (Windows)
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Installez les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurez la base de données MySQL
```bash
mysql -u root -p
```
```sql
CREATE DATABASE emsi_discuss_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Appliquez les migrations
```bash
python manage.py migrate
```

### 6. Créez un super utilisateur
```bash
python manage.py createsuperuser
```

### 7. Lancez le serveur
```bash
python manage.py runserver
```

Accédez à : **http://127.0.0.1:8000/**

## 📖 Documentation Complète

Pour des instructions détaillées, consultez:
- 📄 [COMMANDES_TERMINAL.md](./COMMANDES_TERMINAL.md) - Guide complet des commandes
- 📄 [emsi_discuss/README.md](./emsi_discuss/README.md) - Documentation du projet

## ✨ Contenu du Projet

### ✅ Étape 1 : Initialisation & Base du Projet (COMPLÉTÉE)

- ✓ Projet Django créé et configuré
- ✓ 5 applications créées (accounts, forum, votes, moderation, notifications)
- ✓ Modèles de base définis
- ✓ Admin Django configuré
- ✓ Templates Bootstrap créés
- ✓ Fichiers statiques (CSS, JS) ajoutés
- ✓ URLs configurées
- ✓ Page d'accueil fonctionnelle
- ✓ Documentation complète

### 📋 Applications Incluses

1. **Accounts** - Gestion des utilisateurs et profils
2. **Forum** - Catégories, sous-catégories, sujets et réponses
3. **Votes** - Système de votes utile/pas utile
4. **Moderation** - Signalements et bannissements
5. **Notifications** - Système de notifications

## 🔧 Technologies Utilisées

- **Framework** : Django 4.2
- **Base de données** : MySQL
- **Frontend** : Bootstrap 5
- **Language** : Python

## 📝 Prochaines Étapes

- Développer les templates avancés
- Implémenter les vues détaillées
- Ajouter l'authentification complète
- Mettre en place le système de permissions
- Tests unitaires et intégrés
- Déploiement en production

## ❓ Questions ou Problèmes ?

Consultez le fichier [COMMANDES_TERMINAL.md](./COMMANDES_TERMINAL.md) pour le dépannage.

---

**Dernière mise à jour** : 22 Avril 2024
**Statut** : ✅ Base du projet initialisée avec succès