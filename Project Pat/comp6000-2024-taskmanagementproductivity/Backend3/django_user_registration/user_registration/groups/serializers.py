from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Group

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='members',
        required=False  # 👈 Make member_ids optional
    )
    admin = UserSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ['id','group_name','description','created_by','admin','members', 'member_ids','created_at']
        read_only_fields = ['created_by' , 'admin']  # 👈 Mark created_by as read-only
