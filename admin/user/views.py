# users/views.py
from django.http import JsonResponse

def signup(request):
    return JsonResponse({'message': 'Signup endpoint'})

def login(request):
    return JsonResponse({'message': 'Login endpoint'})