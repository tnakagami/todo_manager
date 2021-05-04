from django.contrib import admin
from . import models

class TaskAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text', 'is_done')
    list_display = ['title', 'is_done', 'point', 'target_date', 'created_at', 'updated_at']
    list_filter = ['is_done']
    ordering = ('-updated_at',)

admin.site.register(models.Task, TaskAdmin)