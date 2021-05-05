from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy
from django.db.models import Q
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

