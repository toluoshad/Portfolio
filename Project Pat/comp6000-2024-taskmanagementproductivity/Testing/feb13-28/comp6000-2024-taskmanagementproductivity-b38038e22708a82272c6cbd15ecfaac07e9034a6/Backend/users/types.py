import graphene
from graphene_django.types import DjangoObjectType

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "username", "is_active", "is_staff",
          'is_superuser',
                  )