from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
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

class CreateUserPage(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        ret = user.is_authenticated and user.is_staff

        return ret

    def get(self, request):
        """
        GETでのリクエスト
        """
        user_form = forms.CreateUserForm()
        profile_form = forms.UserProfileForm()
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        response = render(request, 'account/create_user.html', context)

        return response

    def post(self, request):
        """
        POSTでのリクエスト
        """
        user_form = forms.CreateUserForm(request.POST)
        profile_form = forms.UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Userモデルの処理。ログインできるようis_activeをTrueにし保存
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
            # Profileモデルの処理。Userモデルと紐づける
            profile = profile_form.save(commit=False)
            user.profile.update(profile)
            user.profile.save()
            response = redirect('account:index')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
            }
            response = render(request, 'account/create_user.html', context)

        return response