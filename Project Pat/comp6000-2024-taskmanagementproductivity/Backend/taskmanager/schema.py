import graphene
from users.queries import Query as UsersQuery
from users.mutations import Mutation as UsersMutation

class Query(UsersQuery, graphene.ObjectType):
    pass

class Mutation(UsersMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
