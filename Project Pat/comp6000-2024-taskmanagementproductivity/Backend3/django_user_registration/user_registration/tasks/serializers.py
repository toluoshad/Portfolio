from rest_framework import serializers
from .models import Task
from django.utils import timezone
from .models import Activity

class TaskSerializer(serializers.ModelSerializer):
    # You might want to display the creator's username or other user-specific information
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'created_at', 'updated_at', 'status', 'creator', 'is_overdue', 'project', 'assigned_to', 'priority']
        read_only_fields = ['created_at', 'updated_at']

    def validate_due_date(self, value):
        """
        Check that the due date is not in the past.
        """
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
    
class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Activity
        fields = ['user', 'message', 'timestamp']
