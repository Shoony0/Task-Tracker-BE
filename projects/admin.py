from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Project._meta.fields]
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'description', 'owner__username')
