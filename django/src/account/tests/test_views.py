from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse, resolve
from django.contrib.auth.hashers import make_password
from account.tests.factories import UserFactory, UserModel
from account import views
import random, string

class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.password = 'password'
        cls.user = UserFactory(email='user@example.com', password=make_password(cls.password))

    def chk_class(self, resolver, class_view):
        self.assertEqual(resolver.func.__name__, class_view.__name__)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

class TopPageTests(BaseTestCase):
    def test_top_page_access(self):
        url = reverse('account:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('account/index.html')

    def test_top_page_view(self):
        resolver = resolve('/')
        self.chk_class(resolver, views.TopPage)

class LoginPageTests(BaseTestCase):
    def test_login_page_access(self):
        params = {
            'username': self.user.email,
            'password': self.password,
        }
        url = reverse('account:login')
        response = self.client.post(url, params, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('account/login.html')
        self.assertTrue(response.context['user'].is_authenticated)
        self.client.logout()

    def test_login_page(self):
        resolver = resolve('/login/')
        self.chk_class(resolver, views.LoginPage)

    @override_settings(AXES_ENABLED=False)
    def test_invalid_email_in_login_page(self):
        params = {
            'username': self.user.email + '0',
            'password': self.password,
        }
        url = reverse('account:login')
        response = self.client.post(url, params)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    @override_settings(AXES_ENABLED=False)
    def test_invalid_password_in_login_page(self):
        # check username
        params = {
            'username': self.user.email,
            'password': self.password + '0',
        }
        url = reverse('account:login')
        response = self.client.post(url, params)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

class LogoutPageTests(BaseTestCase):
    @override_settings(AXES_ENABLED=False)
    def setUp(self):
        super().setUp()
        self.client.login(username=self.user.email, password=self.password)

    def test_logout_page_access(self):
        url = reverse('account:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('account/top_page.html')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_page_view(self):
        resolver = resolve('/logout/')
        self.chk_class(resolver, views.LogoutPage)
