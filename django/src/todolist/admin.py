from django.contrib import admin
from . import models

class TaskCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['name',]
    list_filter = []
    ordering = ('-name',)

class TaskAdmin(admin.ModelAdmin):
    search_fields = ('user', 'title', 'text', 'is_done', 'complete_date')
    list_display = ['user', 'title', 'is_done', 'point', 'limit_date', 'complete_date']
    list_filter = ['is_done', 'limit_date']
    ordering = ('-complete_date',)

class PointHistoryAdmin(admin.ModelAdmin):
    search_fields = ('user', 'used_point', 'used_date')
    list_display = ['user', 'used_point', 'used_date']
    list_filter = ['used_point', 'used_date']
    ordering = ('-used_date',)

admin.site.register(models.TaskCategory, TaskCategoryAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.PointHistory, PointHistoryAdmin)