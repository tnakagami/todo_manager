from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
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

class CreateUserForm(UserCreationForm):
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
