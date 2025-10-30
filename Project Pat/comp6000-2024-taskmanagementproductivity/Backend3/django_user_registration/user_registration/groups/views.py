from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Group
from .serializers import GroupSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid():
        # ✅ Save group with the current user as both creator and admin
        group = serializer.save(created_by=request.user, admin=request.user)

        # ✅ Automatically add the creator as a member of the group
        group.members.add(request.user)

        # ✅ Return the group info with the creator included
        return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def get_all_groups(request):
    groups = Group.objects.all().order_by('-created_at')
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_groups(request):
    groups = Group.objects.filter(members=request.user).order_by('-created_at')
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def update_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    serializer = GroupSerializer(group, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_group(request, group_id):
    try:
        group = get_object_or_404(Group, id=group_id)
        
        # Check if the requesting user is the group admin
        if group.admin != request.user:
            return Response(
                {'detail': 'Only the group admin can delete the group.'},
                status=status.HTTP_403_FORBIDDEN
            )
        group.delete()
        return Response(
            {'message': 'Group deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )
        
    except Exception as e:
        return Response(
            {'detail': 'An error occurred while deleting the group.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # ✅ Only allow if requester is already a member
    if request.user not in group.members.all():
        return Response({'detail': 'Only members can add others.'}, status=403)

    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'detail': 'user_id is required.'}, status=400)

    user_to_add = get_object_or_404(User, id=user_id)
    group.members.add(user_to_add)
    return Response({'message': f'{user_to_add.username} added to group.'}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_username(request, username):
    try:
        user = get_user_model().objects.get(username=username)
        return Response({'id': user.id, 'username': user.username})
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_self(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # ❌ Prevent admin from leaving without transferring admin rights
    if group.admin == request.user:
        return Response(
            {'detail': 'You must transfer admin rights before leaving the group.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ✅ Allow member (not admin) to leave
    if request.user in group.members.all():
        group.members.remove(request.user)
        return Response({'message': 'You have left the group.'}, status=status.HTTP_200_OK)

    return Response({'detail': 'You are not a member of this group.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Only the admin can remove members
    if group.admin != request.user:
        return Response({'detail': 'Only the group admin can remove members.'}, status=403)

    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'detail': 'user_id is required.'}, status=400)

    user_to_remove = get_object_or_404(User, id=user_id)

    # Admin cannot remove themselves
    if user_to_remove == request.user:
        return Response({'detail': 'Admin cannot remove themselves.'}, status=400)

    if user_to_remove not in group.members.all():
        return Response({'detail': 'User is not a member of this group.'}, status=400)

    group.members.remove(user_to_remove)
    return Response({'message': f'{user_to_remove.username} has been removed from the group.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_admin(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if group.admin != request.user:
        return Response({'detail': 'Only the current admin can transfer admin rights.'}, status=403)

    new_admin_id = request.data.get('user_id')
    if not new_admin_id:
        return Response({'detail': 'user_id is required.'}, status=400)

    new_admin = get_object_or_404(User, id=new_admin_id)

    if new_admin not in group.members.all():
        return Response({'detail': 'New admin must be a member of the group.'}, status=400)

    group.admin = new_admin
    group.save()
    return Response({'message': f'{new_admin.username} is now the group admin.'})


