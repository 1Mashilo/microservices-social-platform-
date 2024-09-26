"""
This module provides views for user signup and login functionalities in a Django application.
It includes enhanced validation for user input, generates authentication tokens for users, and 
provides a viewset for viewing user profiles.
"""

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.authtoken.models import Token
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Profile
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
import json

@csrf_exempt 
def signup(request):
    """
    Handle user signup requests.

    This view accepts POST requests with JSON data containing 'username', 'password', 'email' (optional), 
    and 'bio' (optional). It performs validation on the input data, creates a new user and profile, 
    and generates an authentication token for the user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response with a token if the signup is successful, or an error message otherwise.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            email = data.get('email', '') 
            bio = data.get('bio', '')  # Get bio from request data (optional)

            # Enhanced validation
            if not username or not password:
                return JsonResponse({'error': 'Please provide both username and password'}, status=400)

            if len(password) < 8:
                return JsonResponse({'error': 'Password must be at least 8 characters long'}, status=400)

            if email:
                try:
                    validate_email(email)
                except ValidationError:
                    return JsonResponse({'error': 'Invalid email address'}, status=400)

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already taken'}, status=400)

            # Create the user
            user = User.objects.create_user(username=username, password=password, email=email)

            # Create the Profile
            Profile.objects.create(user=user, bio=bio)

            # Generate a token for the user
            token, created = Token.objects.get_or_create(user=user)

            return JsonResponse({'token': token.key}, status=201) 

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def user_login(request):
    """
    Handle user login requests.

    This view accepts POST requests with JSON data containing 'username' and 'password'. 
    It authenticates the user and generates an authentication token if the credentials are valid.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response with a token if the login is successful, or an error message otherwise.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']

            if not username or not password:
                return JsonResponse({'error': 'Please provide both username and password'}, status=400)

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({'token': token.key}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows profiles to be viewed.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [] 
