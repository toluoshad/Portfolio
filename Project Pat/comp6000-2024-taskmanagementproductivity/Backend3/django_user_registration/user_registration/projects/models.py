from django.db import models
from django.conf import settings
from django.utils import timezone

class Project(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)  # Both blank and null allowed
    due_date = models.DateField(null=True, blank=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ongoing'
    )
    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True)

    def save(self, *args, **kwargs):
        """Automatically add creator as member when project is created"""
        is_new = self._state.adding  # Check if this is a new project
        super().save(*args, **kwargs)
        if is_new:
            self.users.add(self.creator)  # Add creator as member

    @property
    def member_count(self):
        return self.users.count()

    def __str__(self):
        return self.name