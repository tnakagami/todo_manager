from django.test import TestCase
from django.core import mail
from account.tests.factories import UserFactory, UserModel

class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory(email='alice@example.com', screen_name='_alice13')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

class UserModelTests(BaseTestCase):
    def test_create_user(self):
        self.assertEqual(self.user.get_full_name(), 'alice@example.com')
        self.assertEqual(self.user.get_short_name(), 'alice@example.com')
        self.assertEqual(self.user.screen_name, '_alice13')
        self.assertEqual(self.user.email, 'alice@example.com')
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)

    def test_create_user_blank_screen_name(self):
        blank_screen_name_user = UserFactory(screen_name='')
        self.assertEqual(blank_screen_name_user.screen_name, '')

    def test_create_user_function(self):
        _user = UserModel.objects.create_user(email='user@example.com', password='password')
        self.assertTrue(isinstance(_user, UserModel))

    def test_create_superuser(self):
        _user = UserModel.objects.create_superuser(email='superuser1@example.com', password='admin1password', is_staff=True, is_superuser=True)
        self.assertTrue(isinstance(_user, UserModel))
        self.assertTrue(_user.is_staff)
        self.assertTrue(_user.is_superuser)

        with self.assertRaises(ValueError):
            _ = UserModel.objects.create_superuser(email='superuser2@example.com', password='admin2password', is_staff=True, is_superuser=False)
        with self.assertRaises(ValueError):
            _ = UserModel.objects.create_superuser(email='superuser3@example.com', password='admin3password', is_staff=False, is_superuser=True)

    def test_aux_create_user(self):
        with self.assertRaises(ValueError):
            _ = UserModel.objects._create_user(email='', password='dummy')

    def test_send_mail(self):
        _subject = 'subject name'
        _message = 'sample message'
        self.user.email_user(_subject, _message)
        _outbox = mail.outbox[0]
        self.assertEqual(_outbox.subject, _subject)
        self.assertEqual(_outbox.body, _message)
