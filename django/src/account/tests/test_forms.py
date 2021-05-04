from django.test import TestCase
from account import forms

class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

class LoginFormTests(BaseTestCase):
    def test_valid_form(self):
        params = {
            'username': 'user',
            'password': 'password',
        }
        form = forms.LoginForm(params)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # empty username (= email)
        params = {
            'username': '',
            'password': 'password',
        }
        form = forms.LoginForm(params)
        self.assertFalse(form.is_valid())
        # empty password
        params = {
            'username': 'user',
            'password': '',
        }
        form = forms.LoginForm(params)
        self.assertFalse(form.is_valid())