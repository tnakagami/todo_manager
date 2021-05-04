from django import forms
from . import models

class UpdateTaskStatus(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ('is_done', )