# users/urls.py
from django.urls import path
from .views import signup, login  # We'll create these views later

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
]