from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import ugettext_lazy
from . import models

User = get_user_model()

class LoginForm(AuthenticationForm):
    """
    Login form
    """
    # AuthenticationFormの内容に合わせ、username変数にログイン用のE-mailアドレスを設定する
    username = forms.CharField(label=ugettext_lazy('email address'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class UserSearchForm(forms.Form):
    search_word = forms.CharField(
        label=ugettext_lazy('keyword'),
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': ugettext_lazy('keyword (target: email, screen name)'),
            'class': 'form-control',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def filtered_queryset(self, queryset):
        # get search_word
        search_word = self.cleaned_data.get('search_word')

        if search_word:
            for word in search_word.split():
                queryset = queryset.filter(Q(email__icontains=word) | Q(screen_name__icontains=word))

        return queryset

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'screen_name', 'is_staff')
        widgets = {
            'is_staff': forms.CheckboxInput(attrs={
                'data-toggle': 'toggle',
                'data-onstyle': 'danger',
                'data-offstyle': 'primary',
                'data-width': '200',
                'data-height': '40',
                'data-on': ugettext_lazy('staff user'),
                'data-off': ugettext_lazy('normal user'),
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ('score', 'achievements', 'date_of_birth')
        widgets = {
            'date_of_birth': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'datetimepicker',
                'data-toggle': 'datetimepicker',
                'data-target': '#datetimepicker',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CustomSetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': ugettext_lazy('The two password fields did not match.'),
    }
    new_password1 = forms.CharField(
        label=ugettext_lazy('New password'),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=ugettext_lazy('New password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
        }),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch',)
        password_validation.validate_password(password2, self.user)

        return password2

    def save(self, commit=True):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)

        if commit:
            self.user.save()

        return self.user
