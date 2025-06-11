from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'project', 'status', 'due_date', 'owner')
    list_filter = ('status', 'due_date', 'project')
    search_fields = ('description', 'project__name', 'owner__username')
