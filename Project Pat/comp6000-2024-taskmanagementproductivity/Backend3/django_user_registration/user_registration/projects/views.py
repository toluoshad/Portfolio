from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Project
from .serializers import ProjectSerializer, UserSerializer, AddProjectMemberSerializer

User = get_user_model()

# Create project
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    data = request.data.copy()
    if 'description' in data and data['description'] == '':
        data['description'] = None
    if 'due_date' in data and data['due_date'] == '':
        data['due_date'] = None

    serializer = ProjectSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        project = serializer.save(creator=request.user)
        return Response(ProjectSerializer(project, context={'request': request}).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update project
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    if project.creator != request.user:
        return Response({"error": "You do not have permission"}, status=status.HTTP_403_FORBIDDEN)

    if 'status' in request.data:
        new_status = request.data['status']
        if new_status not in ['ongoing', 'completed']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        project.status = new_status
        project.save()
        return Response({"status": "Status updated successfully"})

    serializer = ProjectSerializer(project, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete project
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)

        if project.creator != request.user:
            return Response({"error": "Permission denied"}, status=403)

        project.delete()
        return Response({"message": "Project deleted successfully"}, status=204)

    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)



# Get all projects for logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_projects(request):
    projects = Project.objects.filter(creator=request.user)
    serializer = ProjectSerializer(projects, many=True, context={'request': request})
    return Response(serializer.data)

# Get project by id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    if project.creator != request.user:
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProjectSerializer(project, context={'request': request})
    return Response(serializer.data)

# Get members of a project
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project_members(request, project_id):
    try:
        project = Project.objects.get(id=project_id, creator=request.user)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)

    serializer = UserSerializer(project.users.all(), many=True)
    return Response(serializer.data)

# Add a member to a project
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_project_member(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Optional: Only the project creator can add members
    if project.creator != request.user:
        return Response({"error": "You do not have permission to add members to this project."},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = AddProjectMemberSerializer(data=request.data, context={
        'request': request,
        'project': project
    })

    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        user = get_object_or_404(User, id=user_id)

        project.users.add(user)

        return Response({
            "message": f"{user.username} has been successfully added to the project."
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ NEW: Get all users for add-member dialog
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_drop(request):
    user = request.user
    return Response({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": getattr(user, 'role', 'User')  # fallback if role field isn't defined
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_username(request, username):
    try:
        user = User.objects.get(username__iexact=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


