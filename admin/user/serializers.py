# users/serializers.py

from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User 

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'bio', 'profile_picture']  # Include 'username'