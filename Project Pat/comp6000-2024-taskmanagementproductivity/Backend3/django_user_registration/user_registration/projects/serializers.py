from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project

User = get_user_model()

# ✅ 1. UserSerializer — for listing project members
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# ✅ 2. ProjectSerializer — matches the fields your JS uses (like member_count, status, creator, etc.)
class ProjectSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    members = UserSerializer(source='users', many=True, read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'due_date',
            'status',
            'creator',
            'members',
            'member_count'
        ]

    def get_member_count(self, obj):
        return obj.users.count()


# ✅ 3. AddProjectMemberSerializer — for validating `user_id` from frontend
# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project

User = get_user_model()

class AddProjectMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return value

    def validate(self, data):
        request = self.context.get("request")
        project = self.context.get("project")
        user_id = data.get("user_id")

        if not request or not project:
            raise serializers.ValidationError("Missing request or project context.")

        if project.users.filter(id=user_id).exists():
            raise serializers.ValidationError("User is already a member of this project.")

        if user_id == request.user.id:
            raise serializers.ValidationError("You are already part of this project.")

        return data
