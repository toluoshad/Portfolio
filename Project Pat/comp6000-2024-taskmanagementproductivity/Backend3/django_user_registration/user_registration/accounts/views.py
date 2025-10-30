from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework import status
from .serializers import UserSerializer
from .serializers import PasswordResetSerializer
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model




# Register user
@api_view(['POST'])
def register_user(request):
    data = request.data
    first_name = data.get('first_name') or data.get('firstName', '').strip()
    last_name = data.get('last_name') or data.get('lastName', '').strip()
    email = data.get('email', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    User = get_user_model()

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    user.first_name = first_name
    user.last_name = last_name
    user.save()


    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

# Login user
@api_view(['POST'])
def login_user(request):
    data = request.data
    username = data.get("username")
    password = data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        # ✅ Generate JWT tokens for authentication
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": "Login successful",
            "refresh": str(refresh),
            "access": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }, status=status.HTTP_200_OK)

    return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

# Delete user account
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # ✅ Only logged-in users can delete their own account
def delete_user(request):
    user = request.user  # ✅ Get the logged-in user

    try:
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Login user
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    User = get_user_model()

    # Check if the user exists
    if not User.objects.filter(username=username).exists():
        return Response({"error": "User not found. Please check your username."}, status=status.HTTP_404_NOT_FOUND)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Incorrect password. Please try again."}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'message': 'Login successful'
    })

# Get user profile
@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user  # Get the authenticated user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
def user_profile_drop(request):
    user = request.user  # Get the authenticated user
    return Response({
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": "Admin"  # Add role or other fields as needed
    })

# Logout user
@api_view(['POST'])
def logout_user(request):
    try:
        refresh_token = request.data.get("refresh")  # Get refresh token from request
        token = RefreshToken(refresh_token)  # Create token object
        token.blacklist()  # Blacklist the token
        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    

# Password reset request
@api_view(['POST'])
def password_reset_request(request):
    serializer = PasswordResetSerializer(data=request.data)

    if serializer.is_valid():
        serializer.send_password_reset_email()
        return Response({"message": "Password reset email sent!"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Password reset confirm 
@api_view(['POST'])
def password_reset_confirm(request):
    token = request.data.get("token")
    uid = request.data.get("uid")
    new_password = request.data.get("new_password")

    User = get_user_model()  # ✅ Fix: Define the User model here

    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensures only authenticated users can access
def get_all_users(request):
    User = get_user_model()  # ✅ Fix: Define the User model here
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Update user profile

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user  # Get the logged-in user

    # Retrieve data from request
    new_username = request.data.get('username')
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    # Update username if provided
    if new_username:
        user.username = new_username

    # Update password if provided
    if new_password:
        if not user.check_password(current_password):
            return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        update_session_auth_hash(request, user)  # Keep the user logged in after password change

    try:
        user.save()
        return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
