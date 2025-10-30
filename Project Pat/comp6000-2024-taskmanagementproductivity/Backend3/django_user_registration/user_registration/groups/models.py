from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Group(models.Model):
    group_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='custom_groups')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_of_groups')  # No unique constraint
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name