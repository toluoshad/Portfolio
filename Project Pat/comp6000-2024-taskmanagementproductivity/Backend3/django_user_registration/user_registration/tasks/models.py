from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User





class Task(models.Model):

    # Link to the Project model
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks')
    
    # Link to user model
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_tasks', blank=True, null=True)
    # Basic task data
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status can be something like 'pending', 'in progress', 'completed'
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='low')
    
    # Link to the User model (assuming you are using Django's built-in User model)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    

    def __str__(self):
        return self.title
    
    # Additional methods can be added here
    def is_overdue(self):
        """Return True if the task is overdue, else False."""
        if self.due_date and timezone.now() > self.due_date:
            return True
        return False
    
class Activity(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"