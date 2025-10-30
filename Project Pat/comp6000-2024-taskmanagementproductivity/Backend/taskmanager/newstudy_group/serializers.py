from rest_framework import serializers
from .models import StudyGroup, Task
from django.contrib.auth.models import User

class StudyGroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)  # Allow adding members

    class Meta:
        model = StudyGroup
        fields = ['id', 'group_name', 'description', 'created_by', 'members', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task_name', 'description', 'due_date', 'status', 'created_by', 'study_group', 'created_at']