from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm
)
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy

User = get_user_model()

class LoginForm(AuthenticationForm):
    """
    Login form
    """
    # AuthenticationFormの内容に合わせ、username変数にログイン用のE-mailアドレスを設定する
    username = forms.CharField(label=ugettext_lazy('e-mail address'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
