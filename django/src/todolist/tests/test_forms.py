from django.test import TestCase
from todolist import forms

class BaseTestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

class UpdateTaskStatusTests(BaseTestClass):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form = forms.UpdateTaskStatus

    def test_form(self):
        data = {
            'is_done': True,
        }
        form = self.form(data)
        self.assertTrue(form.is_valid())

        data = {
            'is_done': False,
        }
        form = self.form(data)
        self.assertTrue(form.is_valid())