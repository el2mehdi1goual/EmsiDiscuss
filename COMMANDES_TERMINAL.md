# 🚀 EMSI_Discuss - Guide d'Exécution

## 📋 Commandes Terminales Nécessaires

### 1️⃣ Créer et Activer l'Environnement Virtuel

**Windows:**
```powershell
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
venv\Scripts\activate
```

**Mac/Linux:**
```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate
```

### 2️⃣ Installer Django et le Connecteur MySQL

```bash
# Installer les dépendances
pip install -r requirements.txt
```

**Ou manuellement :**
```bash
# Django
pip install Django==4.2.0

# Connecteur MySQL
pip install mysqlclient==2.2.0
```

### 3️⃣ Configurer la Base de Données MySQL

```bash
# Accéder à MySQL
mysql -u root -p
```

**Ou pour Windows (si MySQL est dans le PATH):**
```cmd
mysql -u root -p
```

**Dans MySQL, créer la base de données:**
```sql
CREATE DATABASE emsi_discuss_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 4️⃣ Faire les Migrations Django

```bash
# Créer les migrations (à partir du dossier du projet)
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

### 5️⃣ Créer un Super Utilisateur (Admin)

```bash
python manage.py createsuperuser
```

**Répondre aux questions :**
- Username: `admin`
- Email: `admin@emsi.com`
- Password: `votre_mot_de_passe`
- Confirm password: `votre_mot_de_passe`

### 6️⃣ Collecter les Fichiers Statiques

```bash
python manage.py collectstatic --noinput
```

### 7️⃣ Lancer le Serveur

```bash
python manage.py runserver
```

**Le serveur sera disponible sur :**
- 🌐 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 🔐 Admin : [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📝 Résumé des Commandes (Copier-Coller)

### Windows (PowerShell):
```powershell
# 1. Créer environnement
python -m venv venv
venv\Scripts\activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. (Dans MySQL) Créer la base de données
# mysql -u root -p
# CREATE DATABASE emsi_discuss_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 4. Migrations
python manage.py makemigrations
python manage.py migrate

# 5. Créer super utilisateur
python manage.py createsuperuser

# 6. Collecter les statiques
python manage.py collectstatic --noinput

# 7. Lancer le serveur
python manage.py runserver
```

### Mac/Linux (Bash/Zsh):
```bash
# 1. Créer environnement
python3 -m venv venv
source venv/bin/activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. (Dans MySQL) Créer la base de données
# mysql -u root -p
# CREATE DATABASE emsi_discuss_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 4. Migrations
python manage.py makemigrations
python manage.py migrate

# 5. Créer super utilisateur
python manage.py createsuperuser

# 6. Collecter les statiques
python manage.py collectstatic --noinput

# 7. Lancer le serveur
python manage.py runserver
```

---

## 🔍 Vérification

Après avoir lancé le serveur, vous devriez voir :

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Visitez:
- ✅ **Page d'accueil** : http://127.0.0.1:8000/
- ✅ **Admin** : http://127.0.0.1:8000/admin/
- ✅ **Forum** : http://127.0.0.1:8000/forum/
- ✅ **Comptes** : http://127.0.0.1:8000/accounts/

---

## 🛑 Arrêter le Serveur

```bash
# Appuyer sur CTRL + C dans le terminal
# ou Cmd + C sur Mac
```

---

## 🐛 Dépannage

**Erreur MySQL:**
- Vérifier que MySQL est installé et en cours d'exécution
- Vérifier le USER et PASSWORD dans `settings.py`

**Erreur "No module named 'django'":**
- Vérifier que l'environnement virtuel est activé
- Réinstaller les dépendances : `pip install -r requirements.txt`

**Port 8000 déjà utilisé:**
```bash
python manage.py runserver 8001  # Utiliser un autre port
```

---

## 📚 Documentation Utile

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

---

**Prêt à démarrer ? 🎉**

Bonne chance avec EMSI_Discuss !
