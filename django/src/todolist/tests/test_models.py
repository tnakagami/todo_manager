from unittest import mock
from django.test import TestCase
from django.db import IntegrityError, transaction
from django.conf import settings
from django.utils import timezone
from account.tests.factories import UserFactory
from todolist import models

class BaseTestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.users = UserFactory.create_batch(10)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

class TaskTests(BaseTestClass):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model = models.Task

    def setUp(self):
        self.tzinfo = pytz.timezone(settings.TIME_ZONE)

    def __chk_instance_data(self, pk, data):
        task = self.model.objects.get(pk=pk)

        for key, value in data.items():
            self.assertEqual(getattr(task, key), value)
        self.assertEqual(str(task), data['title'])

    def __create_and_save(self, data):
        task = self.model()

        for key, value in data.items():
            setattr(task, key, value)
        task.save()

        return task

    def test_task_is_empty(self):
        self.assertEqual(self.model.objects.count(), 0)

    @mock.patch('django.utils.timezone.now')
    def test_create_task(self, mock_timezone):
        dt = timezone.datetime(2021, 1, 1, tzinfo=tzinfo)
        mock_timezone.return_value = dt
        _user = self.users[0]
        data = {
            'user': _user,
            'title': '_title',
            'text': '_text',
            'is_done': False,
            'point': 1,
        }
        task = self.__create_and_save(data)
        self.assertEqual(self.model.objects.filter(user=_user).count(), 1)
        expected = {key: value for key, value in data.items()}
        expected['target_date'] = dt
        expected['created_at'] = dt
        expected['updated_at'] = dt
        self.__chk_instance_data(task.pk, expected)