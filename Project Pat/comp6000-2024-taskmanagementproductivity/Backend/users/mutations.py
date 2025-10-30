import graphene
from graphql import GraphQLError
from .models import User
from .types import UserType


class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, email, username, password):
        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            raise GraphQLError("Email already in use")

        # Check if username is already in use
        if User.objects.filter(username=username).exists():
            raise GraphQLError("Username already in use")

        # Create and save the new user
        user = User(email=email, username=username)
        user.set_password(password)  # Hash the password
        user.save()

        # Return the created user
        return CreateUser(user=user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)  # Unique identifier for the user

    success = graphene.Boolean()  # Indicates whether the deletion was successful
    message = graphene.String()   # Optional message to return

    def mutate(self, info, id):
        try:
            # Find the user by ID
            user = User.objects.get(id=id)
            # Delete the user
            user.delete()
            # Return success message
            return DeleteUser(success=True, message="User deleted successfully")
        except User.DoesNotExist:
            # Raise an error if the user doesn't exist
            raise GraphQLError("User not found")


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)  # ID of the user to update
        email = graphene.String()        # Optional: New email
        username = graphene.String()     # Optional: New username
        password = graphene.String()     # Optional: New password

    user = graphene.Field(UserType)  # Return the updated user

    def mutate(self, info, id, email=None, username=None, password=None):
        # Fetch the user by ID
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise GraphQLError("User not found")

        # Update the email if provided
        if email is not None:
            if User.objects.filter(email=email).exclude(id=id).exists():
                raise GraphQLError("Email already in use")
            user.email = email

        # Update the username if provided
        if username is not None:
            if User.objects.filter(username=username).exclude(id=id).exists():
                raise GraphQLError("Username already in use")
            user.username = username

        # Update the password if provided
        if password is not None:
            user.set_password(password)

        # Save the updated user
        user.save()

        # Return the updated user
        return UpdateUser(user=user)


# Define the Mutation class at the top level
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    update_user = UpdateUser.Field()