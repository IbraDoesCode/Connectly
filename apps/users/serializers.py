from django.contrib.auth.models import Group
from rest_framework import serializers
from .factories import UserFactory
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(write_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'bio', 'full_name']
        read_only_fields = ['full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')

        profile = UserFactory.create_user_and_profile(
            username=user_data['username'],
            email=user_data['email'],
            password=password,
            **validated_data,
        )

        return profile

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context and self.context['request'].method == 'POST':
            data.pop('full_name', None)
        return data


class RoleSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['Admin', 'Moderator'])

    class Meta:
        model = Group
        fields = ['role']