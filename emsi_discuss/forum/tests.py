"""
Tests pour l'application Forum
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Category, SubCategory, Topic, Tag, Reply


class CategoryTestCase(TestCase):
    """
    Tests pour le modèle Category
    """
    
    def setUp(self):
        self.category = Category.objects.create(name='Django', slug='django')
    
    def test_category_creation(self):
        """Test la création d'une catégorie"""
        self.assertEqual(self.category.name, 'Django')
        self.assertEqual(self.category.slug, 'django')
    
    def test_category_str(self):
        """Test la représentation string"""
        self.assertEqual(str(self.category), 'Django')


class SubCategoryTestCase(TestCase):
    """
    Tests pour le modèle SubCategory
    """
    
    def setUp(self):
        self.category = Category.objects.create(name='Python', slug='python')
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name='Beginners',
            slug='beginners'
        )
    
    def test_subcategory_creation(self):
        """Test la création d'une sous-catégorie"""
        self.assertEqual(self.subcategory.category, self.category)
        self.assertEqual(self.subcategory.name, 'Beginners')
    
    def test_subcategory_str(self):
        """Test la représentation string"""
        expected = f"{self.category.name} > {self.subcategory.name}"
        self.assertEqual(str(self.subcategory), expected)


class TopicTestCase(TestCase):
    """
    Tests pour le modèle Topic
    """
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test', slug='test')
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name='Questions',
            slug='questions'
        )
        self.topic = Topic.objects.create(
            author=self.user,
            subcategory=self.subcategory,
            title='How to Django?',
            content='I have a question about Django'
        )
    
    def test_topic_creation(self):
        """Test la création d'un sujet"""
        self.assertEqual(self.topic.author, self.user)
        self.assertEqual(self.topic.subcategory, self.subcategory)
        self.assertFalse(self.topic.is_solved)
        self.assertFalse(self.topic.is_locked)
    
    def test_topic_get_category(self):
        """Test la méthode get_category"""
        self.assertEqual(self.topic.get_category(), self.category)
    
    def test_topic_increment_views(self):
        """Test l'incrémentation des vues"""
        initial_views = self.topic.views_count
        self.topic.increment_views()
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.views_count, initial_views + 1)


class ReplyTestCase(TestCase):
    """
    Tests pour le modèle Reply
    """
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test', slug='test')
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name='Questions',
            slug='questions'
        )
        self.topic = Topic.objects.create(
            author=self.user,
            subcategory=self.subcategory,
            title='Test Topic',
            content='Test'
        )
        self.reply = Reply.objects.create(
            author=self.user,
            topic=self.topic,
            content='This is a reply'
        )
    
    def test_reply_creation(self):
        """Test la création d'une réponse"""
        self.assertEqual(self.reply.author, self.user)
        self.assertEqual(self.reply.topic, self.topic)
        self.assertFalse(self.reply.is_best_answer)
    
    def test_reply_with_quote(self):
        """Test une réponse avec citation"""
        quoted_reply = Reply.objects.create(
            author=self.user,
            topic=self.topic,
            content='First reply'
        )
        new_reply = Reply.objects.create(
            author=self.user,
            topic=self.topic,
            content='Reply with quote',
            quoted_reply=quoted_reply
        )
        self.assertEqual(new_reply.quoted_reply, quoted_reply)


class TagTestCase(TestCase):
    """
    Tests pour le modèle Tag
    """
    
    def setUp(self):
        self.tag = Tag.objects.create(name='Python', slug='python')
    
    def test_tag_creation(self):
        """Test la création d'un tag"""
        self.assertEqual(self.tag.name, 'Python')
        self.assertEqual(self.tag.slug, 'python')


class ForumViewsTestCase(TestCase):
    """
    Tests pour les vues du forum
    """
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test', slug='test')
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name='Questions',
            slug='questions'
        )
        self.topic = Topic.objects.create(
            author=self.user,
            subcategory=self.subcategory,
            title='Test Topic',
            content='This is a test topic'
        )
    
    def test_forum_home_view(self):
        """Test l'accès à la page d'accueil du forum"""
        response = self.client.get(reverse('forum:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/home.html')
    
    def test_topic_list_view(self):
        """Test l'accès à la liste des sujets"""
        response = self.client.get(reverse('forum:topic_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_list.html')
        self.assertContains(response, 'Test Topic')
    
    def test_topic_detail_view(self):
        """Test l'accès au détail d'un sujet"""
        response = self.client.get(reverse('forum:topic_detail', args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_detail.html')
        self.assertContains(response, 'Test Topic')
    
    def test_topic_create_requires_login(self):
        """Test que la création d'un sujet nécessite une connexion"""
        response = self.client.get(reverse('forum:topic_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_create_topic_view(self):
        """Test la création d'un sujet"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('forum:topic_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_create.html')
    
    def test_reply_create_requires_login(self):
        """Test que la création d'une réponse nécessite une connexion"""
        response = self.client.post(
            reverse('forum:reply_create', args=[self.topic.id]),
            {'content': 'Test reply'}
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_create_reply(self):
        """Test la création d'une réponse"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('forum:reply_create', args=[self.topic.id]),
            {'content': 'This is a test reply'}
        )
        self.assertEqual(response.status_code, 302)  # Redirect to topic detail
        self.assertEqual(Reply.objects.count(), 1)
    
    def test_search_topics(self):
        """Test la recherche de sujets"""
        response = self.client.get(reverse('forum:topic_list'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Topic')
    
    def test_filter_by_category(self):
        """Test le filtrage par catégorie"""
        response = self.client.get(reverse('forum:topic_list'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
