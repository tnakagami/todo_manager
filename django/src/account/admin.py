from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class UserResource(resources.ModelResource):
    class Meta:
        model = User

@admin.register(User)
class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('screen_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'screen_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'screen_name')
    ordering = ('email',)

    # for django-import-exports
    resource_class = UserResource
