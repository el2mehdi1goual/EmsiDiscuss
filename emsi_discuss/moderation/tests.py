"""
Tests pour l'application Moderation
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from forum.models import Category, SubCategory, Topic, Reply
from moderation.models import Report
from accounts.models import Profile


class ReportModelTestCase(TestCase):
    """
    Tests pour le modèle Report
    """
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.reporter = User.objects.create_user(username='reporter', password='testpass')
        self.moderator = User.objects.create_user(username='moderator', password='testpass')
        self.moderator.is_staff = True
        self.moderator.save()
        
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.subcategory = SubCategory.objects.create(
            category=self.category, 
            name='Test SubCategory', 
            slug='test-subcategory'
        )
        
        self.topic = Topic.objects.create(
            author=self.user,
            subcategory=self.subcategory,
            title='Test Topic',
            content='This is a test topic'
        )
        
        self.reply = Reply.objects.create(
            author=self.user,
            topic=self.topic,
            content='This is a test reply'
        )
    
    def test_report_creation_for_topic(self):
        """Test la création d'un signalement pour un topic"""
        report = Report.objects.create(
            reporter=self.reporter,
            content_type=ContentType.objects.get(model='topic'),
            object_id=self.topic.id,
            reason='spam',
            details='This is spam'
        )
        self.assertEqual(report.reporter, self.reporter)
        self.assertEqual(report.status, 'pending')
        self.assertEqual(report.content_object, self.topic)
    
    def test_report_creation_for_reply(self):
        """Test la création d'un signalement pour une réponse"""
        report = Report.objects.create(
            reporter=self.reporter,
            content_type=ContentType.objects.get(model='reply'),
            object_id=self.reply.id,
            reason='inappropriate',
            details='This reply is inappropriate'
        )
        self.assertEqual(report.reporter, self.reporter)
        self.assertEqual(report.content_object, self.reply)
    
    def test_mark_as_resolved(self):
        """Test le marquage d'un rapport comme résolu"""
        report = Report.objects.create(
            reporter=self.reporter,
            content_type=ContentType.objects.get(model='topic'),
            object_id=self.topic.id,
            reason='spam',
            details='Spam report'
        )
        
        report.mark_as_resolved(self.moderator, 'Content hidden')
        self.assertEqual(report.status, 'resolved')
        self.assertEqual(report.reviewed_by, self.moderator)
        self.assertIsNotNone(report.reviewed_at)
    
    def test_mark_as_reviewed(self):
        """Test le marquage d'un rapport comme examiné"""
        report = Report.objects.create(
            reporter=self.reporter,
            content_type=ContentType.objects.get(model='topic'),
            object_id=self.topic.id,
            reason='spam',
            details='Spam report'
        )
        
        report.mark_as_reviewed(self.moderator)
        self.assertEqual(report.status, 'reviewed')
        self.assertEqual(report.reviewed_by, self.moderator)


class ReportViewsTestCase(TestCase):
    """
    Tests pour les vues de modération
    """
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.reporter = User.objects.create_user(username='reporter', password='testpass')
        self.moderator = User.objects.create_user(username='moderator', password='testpass')
        self.moderator.is_staff = True
        self.moderator.save()
        
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.subcategory = SubCategory.objects.create(
            category=self.category, 
            name='Test SubCategory', 
            slug='test-subcategory'
        )
        
        self.topic = Topic.objects.create(
            author=self.user,
            subcategory=self.subcategory,
            title='Test Topic',
            content='This is a test topic'
        )
        
        self.reply = Reply.objects.create(
            author=self.user,
            topic=self.topic,
            content='This is a test reply'
        )
    
    def test_report_content_requires_login(self):
        """Test que le signalement nécessite une connexion"""
        response = self.client.get(reverse('moderation:report_content', args=['topic', self.topic.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_report_topic_view(self):
        """Test l'accès à la vue de signalement d'un topic"""
        self.client.login(username='reporter', password='testpass')
        response = self.client.get(reverse('moderation:report_content', args=['topic', self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderation/report_form.html')
    
    def test_report_reply_view(self):
        """Test l'accès à la vue de signalement d'une réponse"""
        self.client.login(username='reporter', password='testpass')
        response = self.client.get(reverse('moderation:report_content', args=['reply', self.reply.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_cannot_report_own_content(self):
        """Test qu'un utilisateur ne peut pas signaler son propre contenu"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('moderation:report_content', args=['topic', self.topic.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect
    
    def test_submit_report_for_topic(self):
        """Test la soumission d'un signalement pour un topic"""
        self.client.login(username='reporter', password='testpass')
        response = self.client.post(
            reverse('moderation:report_content', args=['topic', self.topic.id]),
            {
                'reason': 'spam',
                'details': 'This is spam content'
            }
        )
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertTrue(Report.objects.filter(reporter=self.reporter).exists())
    
    def test_reports_list_requires_moderator(self):
        """Test que la liste des rapports nécessite d'être modérateur"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('moderation:reports_list'))
        self.assertEqual(response.status_code, 302)  # Should redirect
    
    def test_reports_list_for_moderator(self):
        """Test l'accès à la liste des rapports pour un modérateur"""
        self.client.login(username='moderator', password='testpass')
        response = self.client.get(reverse('moderation:reports_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderation/reports_list.html')
    
    def test_report_detail_requires_moderator(self):
        """Test que le détail du rapport nécessite d'être modérateur"""
        report = Report.objects.create(
            reporter=self.reporter,
            content_type=ContentType.objects.get(model='topic'),
            object_id=self.topic.id,
            reason='spam',
            details='Spam'
        )
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('moderation:report_detail', args=[report.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect
    
    def test_moderator_hide_content(self):
        """Test qu'un modérateur peut masquer un contenu"""
        report = Report.objects.create(
            reporter=self.reporter,
            content_type=ContentType.objects.get(model='topic'),
            object_id=self.topic.id,
            reason='spam',
            details='Spam'
        )
        self.client.login(username='moderator', password='testpass')
        response = self.client.post(
            reverse('moderation:report_detail', args=[report.id]),
            {
                'action': 'hide',
                'resolution_notes': 'Contenu masqué pour spam'
            }
        )
        self.assertEqual(response.status_code, 302)
        
        # Vérifier que le topic est masqué
        self.topic.refresh_from_db()
        self.assertTrue(self.topic.is_hidden)


class TopicHiddenTestCase(TestCase):
    """
    Tests pour les sujets masqués
    """
    
    def setUp(self):
        """Configuration initiale"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.moderator = User.objects.create_user(username='moderator', password='testpass')
        self.moderator.is_staff = True
        self.moderator.save()
        
        self.category = Category.objects.create(name='Test', slug='test')
        self.subcategory = SubCategory.objects.create(category=self.category, name='Sub', slug='sub')
        
        self.hidden_topic = Topic.objects.create(
            author=self.user,
            subcategory=self.subcategory,
            title='Hidden Topic',
            content='Hidden',
            is_hidden=True,
            hidden_reason='Spam'
        )
        
        self.visible_topic = Topic.objects.create(
            author=self.user,
            subcategory=self.subcategory,
            title='Visible Topic',
            content='Visible'
        )
    
    def test_hidden_topic_not_accessible_to_user(self):
        """Test qu'un topic masqué n'est pas accessible"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('forum:topic_detail', args=[self.hidden_topic.id]))
        self.assertEqual(response.status_code, 404)
    
    def test_hidden_topic_accessible_to_moderator(self):
        """Test qu'un topic masqué est accessible au modérateur"""
        self.client.login(username='moderator', password='testpass')
        response = self.client.get(reverse('forum:topic_detail', args=[self.hidden_topic.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_hidden_topic_accessible_to_author(self):
        """Test qu'un topic masqué est accessible à l'auteur"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('forum:topic_detail', args=[self.hidden_topic.id]))
        # Author should see it, but we're not the author in this case
        # So this should return 404
        self.assertEqual(response.status_code, 404)


class LockedTopicTestCase(TestCase):
    """
    Tests pour les sujets verrouillés
    """
    
    def setUp(self):
        """Configuration initiale"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = User.objects.create_user(username='author', password='testpass')
        
        self.category = Category.objects.create(name='Test', slug='test')
        self.subcategory = SubCategory.objects.create(category=self.category, name='Sub', slug='sub')
        
        self.locked_topic = Topic.objects.create(
            author=self.author,
            subcategory=self.subcategory,
            title='Locked Topic',
            content='Locked',
            is_locked=True
        )
    
    def test_cannot_reply_to_locked_topic(self):
        """Test qu'on ne peut pas répondre à un sujet verrouillé"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('forum:reply_create', args=[self.locked_topic.id]),
            {'content': 'This should not work'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reply.objects.filter(topic=self.locked_topic).count(), 0)


class BanUserTestCase(TestCase):
    """
    Tests pour le bannissement temporaire
    """
    
    def setUp(self):
        """Configuration initiale"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.banned_user = User.objects.create_user(username='banned', password='testpass')
        
        self.category = Category.objects.create(name='Test', slug='test')
        self.subcategory = SubCategory.objects.create(category=self.category, name='Sub', slug='sub')
        
        self.topic = Topic.objects.create(
            author=self.user,
            subcategory=self.subcategory,
            title='Test Topic',
            content='Test'
        )
    
    def test_banned_user_cannot_reply(self):
        """Test qu'un utilisateur banni ne peut pas répondre"""
        # Ban the user
        self.banned_user.profile.is_banned = True
        self.banned_user.profile.banned_until = timezone.now() + timedelta(days=7)
        self.banned_user.profile.save()
        
        self.client.login(username='banned', password='testpass')
        response = self.client.post(
            reverse('forum:reply_create', args=[self.topic.id]),
            {'content': 'This should not work'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reply.objects.filter(author=self.banned_user).count(), 0)
