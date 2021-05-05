from unittest import mock
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse, resolve
from account.tests.factories import UserFactory
from todolist.tests.factories import TaskFactory
from todolist import views, models

class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.password = 'password'
        cls.users = UserFactory.create_batch(3)
        cls.no_task_user = UserFactory(email='no_task@example.com', screen_name='no_task')
        cls.tasks = [TaskFactory.create(user=_user, score=1) for _user in cls.users] + [TaskFactory.create(user=_user, is_done=True, score=3) for _user in cls.users]
        cls.superuser = UserFactory(email='superuser@example.com', screen_name='superuser', is_staff=True, is_superuser=True)
        cls.staff = UserFactory(email='staff@example.com', screen_name='staff', is_staff=True)

    def chk_class(self, resolver, class_view):
        self.assertEqual(resolver.func.__name__, class_view.__name__)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

class ToDoListTests(BaseTestCase):
    @override_settings(AXES_ENABLED=False)
    def setUp(self):
        self.client.login(username=self.users[0].email, password=self.password)
        self.url = reverse('todolist:index')

    def test_resolve_url(self):
        resolver = resolve('/todolist/')
        self.chk_class(resolver, views.ToDoList)

    def test_no_login_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    @override_settings(AXES_ENABLED=False)
    def test_no_tasks(self):
        self.client.logout()
        self.client.login(username=self.no_task_user.email, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('tasks' in response.context.keys())
        self.assertTrue('aggregated' in response.context.keys())
        _tasks = response.context.get('tasks')
        _aggregated = response.context.get('aggregated')
        self.assertEqual(len([task for task in _tasks if task.user == self.no_task_user]), 0)
        self.assertEqual(len([data for data in _aggregated if task['email'] == self.no_task_user.email]), 0)

    def test_filtered_task(self):
        _user = self.users[0]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        _tasks = response.context.get('tasks')
        _aggregated = response.context.get('aggregated')
        self.assertEqual(len([task for task in _tasks if task.user == _user]), 2)
        for data in _aggregated:
            self.assertEqual(data['email'], _user.email)
            self.assertEqual(data['screen_name'], _user.screen_name)
            self.assertEqual(data['finished'], 1)
            self.assertEqual(data['total'], 2)
            self.assertEqual(data['score'], 3)