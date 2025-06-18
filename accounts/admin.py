from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [field.name for field in User._meta.fields]
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'roles')
    search_fields = ('username', 'email')
    filter_horizontal = ('roles', 'groups', 'user_permissions')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Role._meta.fields]
    search_fields = ('name',)
