import graphene
from users.queries import Query as UsersQuery
from users.mutations import Mutation as UsersMutation

# Combine queries and mutations into a single schema
class Query(UsersQuery, graphene.ObjectType):
    pass

class Mutation(UsersMutation, graphene.ObjectType):
    pass

# Define the schema
schema = graphene.Schema(query=Query, mutation=Mutation)