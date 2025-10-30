import graphene
from graphql import GraphQLError
from .models import User
from .types import UserType

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType, description="Fetch all users.")

    def resolve_all_users(self, info):
        """
        Resolver for fetching all users.
        """
        return User.objects.all()

    user = graphene.Field(
        UserType,
        id=graphene.Int(required=True, description="The ID of the user to fetch."),
        description="Fetch a single user by ID.",
    )

    def resolve_user(self, info, id):
        """
        Resolver for fetching a single user by ID.
        """
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise GraphQLError(f"User with ID {id} does not exist.")
