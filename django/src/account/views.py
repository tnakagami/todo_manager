from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.views.generic import TemplateView
from . import forms

User = get_user_model()

class TopPage(TemplateView):
    """
    Top Page
    """
    template_name = 'account/index.html'

class LoginPage(LoginView):
    """
    Login Page
    """
    form_class = forms.LoginForm
    template_name = 'account/login.html'

class LogoutPage(LogoutView):
    """
    Logout Page
    """
    template_name = 'account/index.html'