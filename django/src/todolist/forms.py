from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy
from . import models

User = get_user_model()

class UpdateTaskStatus(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ('is_done', )

class CreateTaskCategory(forms.ModelForm):
    class Meta:
        model = models.TaskCategory
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CreateTask(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ('user', 'title', 'text', 'point', 'category', 'limit_date')
        widgets = {
            'user': forms.Select(attrs={
                    'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'placeholder': ugettext_lazy('Markdown support\n\n## Introduction\nThis is sample text.'),
                'rows': 20, 'cols': 10, 'style': 'resize:none;',
                'class': 'form-control',
            }),
            'point': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                    'class': 'form-control',
            }),
            'limit_date': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'datetimepicker',
                'data-toggle': 'datetimepicker',
                'data-target': '#datetimepicker',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].queryset = User.objects.filter(is_staff=False)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
