from django.db import models
from accounts.models import User
from projects.models import Project

STATUS_CHOICES = [
    ("new", "New"),
    ("in_progress", "In Progress"),
    ("blocked", "Blocked"),
    ("completed", "Completed"),
    ("not_started", "Not Started"),
]

class Task(models.Model):
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(User, related_name="tasks", on_delete=models.SET_NULL, null=True)
    
