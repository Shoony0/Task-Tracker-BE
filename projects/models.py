from django.db import models
from accounts.models import User

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.name  
