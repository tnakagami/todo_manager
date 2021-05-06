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

class UserProfilePageTests(BaseTestCase):
    @override_settings(AXES_ENABLED=False)
    def setUp(self):
        super().setUp()
        self.client.login(username=self.user.email, password=self.password)

    def test_user_profile_page_access(self):
        url = reverse('account:user_profile')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('account/user_profile.html')

    def test_user_profile_page_view(self):
        resolver = resolve('/profile/')
        self.chk_class(resolver, views.UserProfilePage)

class CreateUserPageTests(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.superuser = UserFactory(email='superuser@example.com', password=make_password(cls.password))
        cls.staffuser = UserFactory(email='staffuser@example.com', password=make_password(cls.password))

    @override_settings(AXES_ENABLED=False)
    def test_access_for_normaluser(self):
        self.client.login(username=self.user.email, password=self.password)
        url = reverse('account:create_user')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    @override_settings(AXES_ENABLED=False)
    def test_access_for_staffuser(self):
        self.client.login(username=self.staffuser.email, password=self.password)
        url = reverse('account:create_user')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('account/create_user.html')
        self.assertTrue('user_form' in response.context.keys())
        self.assertTrue('profile_form' in response.context.keys())

    @override_settings(AXES_ENABLED=False)
    def test_access_for_superuser(self):
        self.client.login(username=self.superuser.email, password=self.password)
        url = reverse('account:create_user')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_create_user_page_view(self):
        resolver = resolve('/create_user/')
        self.chk_class(resolver, views.CreateUserPage)
