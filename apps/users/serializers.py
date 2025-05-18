from django.contrib.auth.models import Group, User
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .factories import UserFactory
from .models import Profile, Follow
from ..posts.models import Post


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    posts_count = serializers.SerializerMethodField(read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)
    profile_image = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'bio', 'full_name', 'is_following', 'created_at', 'posts_count', 'followers', 'following', 'profile_image', 'cover_image']
        read_only_fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def get_is_following(self, obj):
        user = self.context['request'].user
        return Follow.objects.filter(follower=user, followed=obj.user).exists()
    
    def get_posts_count(self, obj):
        return Post.objects.filter(author=obj.user).count()
    
    def get_followers(self, obj):
        return Follow.objects.filter(followed=obj.user).count()

    def get_following(self, obj):
        return Follow.objects.filter(follower=obj.user).count()
    
    def get_profile_image(self, obj):
        return obj.profile_image.url if obj.profile_image else None
    
    def get_cover_image(self, obj):
        return obj.cover_image.url if obj.cover_image else None

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        password = validated_data.pop('password', None)

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

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def update(self, instance, validated_data):
        """Update the user instance with validated data."""
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class RoleSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['Admin', 'Moderator'])

    class Meta:
        model = Group
        fields = ['role']


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if ('first_name' in data and not last_name) or ('last_name' in data and not first_name):
            raise serializers.ValidationError(
                "Both 'first_name' and 'last_name' are required when updating either."
            )

        return data

    class Meta:
        model = Profile
        fields = ['id', 'user', 'first_name', 'last_name', 'bio', 'profile_image', 'cover_image']


class ProfileBasicSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    full_name = serializers.SerializerMethodField(read_only=True)
    profile_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'full_name', 'profile_image']

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


        
class ProfileSearchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'full_name']
        read_only_fields = ['id', 'username', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class FollowSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Follow
        fields = ['user_id', 'created_at']

    def validate_user_id(self, value):
        try:
            user_to_follow = User.objects.get(id=value)
        except User.DoesNotExist:
            raise ValidationError("User to follow does not exist.")
        
        if self.context['request'].user == user_to_follow:
            raise ValidationError("You cannot follow yourself.")
        
        return user_to_follow

    def validate(self, data):
        user_to_follow = data['user_id']
        follower = self.context['request'].user

        # Check if a follow record exists
        follow_instance = Follow.objects.filter(follower=follower, followed=user_to_follow).first()

        if follow_instance:
            data['to_unfollow'] = follow_instance
        else:
            data['followed'] = user_to_follow
            data['follower'] = follower
        return data

    def create(self, validated_data):
        if 'to_unfollow' in validated_data:
            validated_data['to_unfollow'].delete()
            return {'Unfollowed': True}

        validated_data.pop('user_id')
        return Follow.objects.create(**validated_data)