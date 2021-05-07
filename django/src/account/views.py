from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, ListView, UpdateView, View, FormView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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

class UserProfilePage(LoginRequiredMixin, TemplateView):
    """
    Profile Page
    """
    template_name = 'account/user_profile.html'

class StaffUserMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        ret = user.is_authenticated and user.is_staff

        return ret

class RegisteredUserPage(StaffUserMixin, ListView):
    model = User
    template_name = 'account/registered_user.html'
    paginate_by = 100
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_staff=False)
        form = forms.UserSearchForm(self.request.GET or None)
 
        # check form
        if form.is_valid():
            queryset = form.filtered_queryset(queryset)
        # ordering
        queryset = queryset.order_by('pk')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = forms.UserSearchForm(self.request.GET or None)

        return context

class CreateUserPage(StaffUserMixin, View):
    def get(self, request):
        """
        GETでのリクエスト
        """
        user_form = forms.CustomUserCreationForm()
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
        user_form = forms.CustomUserCreationForm(request.POST)
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
            response = redirect('account:registered_user')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
            }
            response = render(request, 'account/create_user.html', context)

        return response

class UpdateUserProfilePage(StaffUserMixin, UpdateView):
    model = User
    form_class = forms.UserProfileForm
    template_name = 'account/update_user_profile.html'
    context_object_name = 'target_user'
    success_url = reverse_lazy('account:registered_user')

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        ret = user.is_authenticated and (user.pk == self.kwargs['pk'] or user.is_staff)

        return ret

class SetPasswordPage(OnlyYouMixin, FormView):
    form_class = forms.CustomSetPasswordForm
    template_name = 'account/set_password.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.user = User.objects.get(pk=self.kwargs['pk'])
        kwargs['user'] = self.user

        return kwargs

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user

        if user.is_staff:
            response = reverse_lazy('account:registered_user')
        else:
            # login
            auth_login(self.request, self.user, backend='django.contrib.auth.backends.ModelBackend')
            response = reverse_lazy('account:user_profile')

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_user'] = self.user

        return context