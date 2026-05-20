# 📊 FLUX COMPLET DE CRÉATION D'UN SUJET

## PHASE 1️⃣: LE CLIC SUR "CRÉER UN SUJET"

```
1. Utilisateur clique sur le bouton "Créer un Sujet" 
   → URL: /forum/topic/create/
   → GET REQUEST
```

**URL Routing** (`forum/urls.py`):
```python
path('topic/create/', views.topic_create, name='topic_create')
```

---

## PHASE 2️⃣: AFFICHAGE DU FORMULAIRE (GET)

```
2. Django appelle la vue topic_create() avec method='GET'
   
3. La vue crée un formulaire VIDE:
   form = TopicCreateForm()
   
4. Le formulaire s'affiche dans le template topic_create.html
```

**Template affiche:**
```html
<form method="post" novalidate>
  • Catégorie (dropdown dynamique)
  • Sous-catégorie (dropdown qui se remplit après choix catégorie)
  • Ou créer une nouvelle sous-catégorie (champ texte)
  • Titre du sujet
  • Contenu du sujet (textarea)
  • Tags (Ex: #python #django)
  • Case à cocher "Poster anonyme"
  • Bouton SUBMIT
```

**JavaScript côté client** (dans le navigateur):
```javascript
// Quand l'utilisateur change la catégorie
#id_category change → Appel AJAX
   ↓
GET /forum/api/subcategories/{category_id}/
   ↓
Reçoit les sous-catégories de cette catégorie
   ↓
Remplit le dropdown des sous-catégories dynamiquement
```

---

## PHASE 3️⃣: L'UTILISATEUR REMPLIT LE FORMULAIRE

```
Utilisateur tape:
├─ Catégorie: "Développement Web"
├─ Sous-catégorie: "Django" (ou crée "Django Advanced")
├─ Titre: "Problème avec les migrations Django"
├─ Contenu: "J'ai une erreur quand je lance migrate..."
├─ Tags: "#django #migrations #database"
└─ Anonyme: ☐ (non coché)

Puis clique sur "Créer le sujet"
   ↓
POST REQUEST vers /forum/topic/create/
```

---

## PHASE 4️⃣: VALIDATION (POST)

```
4. La vue reçoit les données POST
   form = TopicCreateForm(request.POST)
   
5. Validation du formulaire:
   ✓ Titre: max 200 caractères, requis
   ✓ Contenu: min X caractères, requis
   ✓ Catégorie: requise
   ✓ Sous-catégorie: requise (soit existante soit nouvelle)
   
   if form.is_valid():
       → PASSER À PHASE 5
   else:
       → Redirection au formulaire avec erreurs affichées
```

---

## PHASE 5️⃣: TRAITEMENT ET SAUVEGARDE EN BD

```
6. Extraire les données validées:
   ├─ category = form.cleaned_data.get('category')
   ├─ subcategory = form.cleaned_data.get('subcategory')
   ├─ new_subcategory_name = form.cleaned_data.get('new_subcategory_name')
   └─ tag_names_str = "#django #migrations"
   
7. Gestion de la SOUS-CATÉGORIE:
   
   Si new_subcategory_name est fourni:
      → SubCategory.objects.get_or_create(
           category=category,
           name="Django Advanced"
        )
      → Crée ou récupère la sous-catégorie
   
   Sinon:
      → Utilise la subcategory existante
      
8. CRÉER LE TOPIC (sauvegarder en BD):
   
   topic = form.save(commit=False)  # Ne pas sauvegarder encore
   topic.author = request.user      # Assigner l'auteur (user connecté)
   topic.subcategory = subcategory  # Assigner la sous-catégorie
   topic.is_solved = False          # Pas encore résolu
   topic.is_locked = False          # Pas verrouillé
   topic.is_pinned = False          # Pas épinglé
   topic.is_hidden = False          # Visible par défaut
   topic.views_count = 0            # Zéro vue au départ
   topic.save()                     # ✅ SAUVEGARDER EN BD
   
   # Topic ID généré automatiquement par Django (auto-increment)
```

**CE QUI SE PASSE EN BD (PostgreSQL/SQLite):**
```sql
INSERT INTO forum_topic 
  (author_id, subcategory_id, title, content, is_anonymous, 
   is_solved, is_locked, is_pinned, is_hidden, views_count, created_at, updated_at)
VALUES 
  (5, 12, 'Problème avec les migrations Django', '...contenu...', 
   false, false, false, false, false, 0, NOW(), NOW())

RETURNING id;  -- Retourne l'ID du nouveau topic (ex: 42)
```

---

## PHASE 6️⃣: TRAITEMENT DES TAGS

```
9. Parser la chaîne "#django #migrations" en liste:
   
   parse_tag_names("#django #migrations")
   → ['django', 'migrations']
   
10. Créer ou récupérer les tags:
   
   For each tag_name in ['django', 'migrations']:
      → Tag.objects.get_or_create(
           name__iexact='django',  # Case-insensitive
           defaults={'name': 'django', 'slug': 'django'}
        )
      → Si tag n'existe pas: CRÉER
      → Si tag existe: RÉCUPÉRER
      
11. Associer les tags au topic (table Many-to-Many):
   
   topic.tags.set([tag_django, tag_migrations])
   
   # Cela crée des lignes dans la table forum_topic_tags
```

**CE QUI SE PASSE EN BD:**
```sql
-- Table forum_topic_tags (Many-to-Many)
INSERT INTO forum_topic_tags (topic_id, tag_id) VALUES (42, 7);   -- Django
INSERT INTO forum_topic_tags (topic_id, tag_id) VALUES (42, 15);  -- Migrations
```

---

## PHASE 7️⃣: PERMISSIONS & BANNISSEMENTS

```
12. Avant tout, vérifier si l'utilisateur est banni:
   
   profile = request.user.profile
   if profile.is_currently_banned():
       → Afficher erreur "Vous êtes banni"
       → Rediriger vers forum:topic_list
       → NE PAS créer le topic
   
   profile.clear_expired_ban()  # Effacer les anciens bans
```

---

## PHASE 8️⃣: MESSAGE DE SUCCÈS & REDIRECTION

```
13. Ajouter un message de succès à la session:
   
   messages.success(request, 'Votre sujet a été créé avec succès !')
   
14. REDIRECTION vers la page du topic:
   
   return redirect('forum:topic_detail', topic_id=42)
   
   URL générée: /forum/topic/42/
```

---

## PHASE 9️⃣: AFFICHAGE DU TOPIC (GET)

```
15. L'utilisateur arrive sur /forum/topic/42/
    
    topic_detail() est appelée:
    
    ├─ Récupère le topic: topic = get_object_or_404(Topic, id=42)
    ├─ Incrémente les vues: topic.increment_views()
    ├─ Récupère les réponses: replies = topic.replies.all()
    ├─ Récupère les votes: votes = TopicVote.objects.filter(topic=topic)
    └─ Rend le template avec tous les données
    
16. Le template topic_detail.html affiche:
    ├─ Titre: "Problème avec les migrations Django"
    ├─ Contenu: "J'ai une erreur..."
    ├─ Auteur: "Ahmed" (ou "Anonyme")
    ├─ Tags: #django #migrations (avec liens cliquables)
    ├─ Section des réponses (vide au départ)
    ├─ Formulaire pour répondre
    └─ Boutons de vote (utile/pas utile)
```

---

## 📦 RÉSUMÉ DES DONNÉES SAUVEGARDÉES

```
✅ Topic créé dans: forum_topic
   ├─ id: 42 (auto-généré)
   ├─ author_id: 5 (ID de l'utilisateur connecté)
   ├─ subcategory_id: 12 (Django Advanced)
   ├─ title: "Problème avec les migrations Django"
   ├─ content: "..."
   ├─ is_anonymous: False
   ├─ created_at: 2026-05-20 10:30:15
   └─ updated_at: 2026-05-20 10:30:15

✅ SubCategory créée si nouvelle: forum_subcategory
   ├─ id: 12
   ├─ category_id: 1 (Développement Web)
   ├─ name: "Django Advanced"
   └─ slug: "django-advanced"

✅ Tags créés/liés: forum_tag + forum_topic_tags
   ├─ tag_id: 7 → topic_id: 42
   └─ tag_id: 15 → topic_id: 42
```

---

## 🔄 VUE D'ENSEMBLE DU FLUX

```
┌─────────────────────────────────────────┐
│ 🎯 CLIC "CRÉER UN SUJET"                │
│ GET /forum/topic/create/                │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 📝 FORMULAIRE VIDE S'AFFICHE            │
│ (avec catégories + sous-catégories)     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ ⌨️ UTILISATEUR REMPLIT LE FORM           │
│ (titre, contenu, catégorie, tags)       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ ✉️ CLIQUE SUBMIT                        │
│ POST /forum/topic/create/               │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ ✅ VALIDATION DES DONNÉES               │
│ (form.is_valid())                       │
└─────────────────────────────────────────┘
                    ↓
        ┌──────────────────────┐
        │ Erreurs? │ Valide?  │
        └──────────────────────┘
              ↙            ↘
          ❌              ✅
       Afficher        Continuer
       Erreurs
                    ↓
┌─────────────────────────────────────────┐
│ 💾 CRÉER LA SOUS-CATÉGORIE (si nouvelle)│
│ SubCategory.objects.get_or_create()     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 💾 CRÉER LE TOPIC                       │
│ topic.save()                            │
│ → INSERT INTO forum_topic               │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 💾 CRÉER/LIER LES TAGS                  │
│ topic.tags.set(tags)                    │
│ → INSERT INTO forum_topic_tags          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ ✅ MESSAGE DE SUCCÈS                    │
│ messages.success()                      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 🔄 REDIRECTION                          │
│ redirect('forum:topic_detail', id=42)   │
│ → GET /forum/topic/42/                  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 📺 AFFICHAGE DU TOPIC                   │
│ topic_detail() rend le template         │
│ avec titre, contenu, tags, réponses...  │
└─────────────────────────────────────────┘
```

---

## 📋 CODE SIMPLIFIÉ DE LA VUE

```python
@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def topic_create(request):
    """Créer un nouveau sujet"""
    
    # Vérifier si l'utilisateur est banni
    profile = request.user.profile
    if profile.is_currently_banned():
        messages.error(request, 'Vous êtes banni.')
        return redirect('forum:topic_list')
    
    if request.method == 'POST':
        form = TopicCreateForm(request.POST)
        
        if form.is_valid():
            # Extraire données
            category = form.cleaned_data.get('category')
            subcategory = form.cleaned_data.get('subcategory')
            new_subcategory_name = form.cleaned_data.get('new_subcategory_name', '').strip()
            tag_names_str = form.cleaned_data.get('tag_names', '')
            
            # Créer ou récupérer la sous-catégorie
            if new_subcategory_name:
                subcategory, created = SubCategory.objects.get_or_create(
                    category=category,
                    name=new_subcategory_name,
                    defaults={'slug': slugify(new_subcategory_name)}
                )
            
            # Créer le topic
            topic = form.save(commit=False)
            topic.author = request.user
            topic.subcategory = subcategory
            topic.save()  # ✅ BD: INSERT INTO forum_topic
            
            # Créer/lier les tags
            tag_names_list = parse_tag_names(tag_names_str)
            tags = get_or_create_tags(tag_names_list)
            topic.tags.set(tags)  # ✅ BD: INSERT INTO forum_topic_tags
            
            messages.success(request, 'Sujet créé avec succès !')
            return redirect('forum:topic_detail', topic_id=topic.id)
    else:
        form = TopicCreateForm()
    
    return render(request, 'forum/topic_create.html', {
        'page_title': 'Créer un Sujet',
        'form': form,
        'action': 'Créer',
    })
```

---

Voilà le flux complet! 🚀
