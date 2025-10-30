from django.db import models
from django.contrib.auth.models import User  # Import Django's built-in User model

class StudyGroup(models.Model):
    group_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')  # User who created the group
    members = models.ManyToManyField(User, related_name='study_groups')  # Users who are members of the group
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name

class Task(models.Model):
    task_name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=50, default='Pending')  # e.g., Pending, In Progress, Completed
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')  # User who created the task
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='tasks')  # Task belongs to a study group
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name