from rest_framework import serializers
from .models import User
from ..posts.serializers import PostSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at']