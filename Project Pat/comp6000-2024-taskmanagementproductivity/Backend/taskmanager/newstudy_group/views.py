from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StudyGroup, Task
from .serializers import StudyGroupSerializer, TaskSerializer
from django.contrib.auth.models import User

# Create a study group
@api_view(['POST'])
def create_study_group(request):
    serializer = StudyGroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Add a member to a study group
@api_view(['POST'])
def add_member_to_group(request, group_id):
    try:
        group = StudyGroup.objects.get(id=group_id)  # Get the study group
    except StudyGroup.DoesNotExist:
        return Response({"error": "Study group not found"}, status=status.HTTP_404_NOT_FOUND)

    user_id = request.data.get('user_id')  # Get the user ID from the request
    if not user_id:
        return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)  # Get the user
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Add the user to the group
    group.members.add(user)
    group.save()

    # Return the updated study group
    serializer = StudyGroupSerializer(group)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Create a task for a study group
@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get all tasks for a study group
@api_view(['GET'])
def get_tasks_for_group(request, group_id):
    try:
        group = StudyGroup.objects.get(id=group_id)  # Get the study group
    except StudyGroup.DoesNotExist:
        return Response({"error": "Study group not found"}, status=status.HTTP_404_NOT_FOUND)

    tasks = group.tasks.all()  # Get all tasks for the group
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)