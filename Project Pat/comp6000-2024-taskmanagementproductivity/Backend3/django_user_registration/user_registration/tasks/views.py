from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework import status

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from .models import Task
from .serializers import TaskSerializer
from .models import Activity
from .serializers import ActivitySerializer

# Create task
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    # Create a copy of the data to modify it
    data = request.data.copy()
    # Initialize the serializer with data and no instance
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        # Save the task instance with the additional creator field set to the current user
        task = serializer.save(creator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update task
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if task.creator != request.user:
        return Response({"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete task
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if task.creator != request.user:
        return Response({"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    
    task.delete()
    return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Get all tasks
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_tasks(request):
    tasks = Task.objects.filter(creator=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

# Get task by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if task.creator != request.user:
        return Response({"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = TaskSerializer(task)
    return Response(serializer.data)

# Get all tasks assigned to the current user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_assigned_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

# Activity feed
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_feed(request):
    activities = Activity.objects.order_by('-timestamp')[:10]
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)