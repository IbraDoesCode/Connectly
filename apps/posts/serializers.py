from django.core.exceptions import ValidationError, PermissionDenied
from rest_framework import serializers

from .factories import PostFactory, CommentFactory
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'comment_type', 'created_at']
        # extra_kwargs = {'post': {'read_only': True}, 'author': {'read_only': True}}

    def validate_content(self, value):
        if not value.strip():
            raise ValidationError('Comment cannot be empty')
        return value
        
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['author'] = instance.author.username if instance.author else None
    #     return response

    def create(self, validated_data):
        print(validated_data)
        return CommentFactory.create_comment(**validated_data)
        
    def update(self, instance, validated_data):
        # Validate that the post is the same as the original
        if instance.post != validated_data.get('post', instance.post):
            raise serializers.ValidationError("You cannot change the post of a comment.")
        
        # Validate that the author is the same as the original
        if instance.author != validated_data.get('author', instance.author):
            raise serializers.ValidationError("You cannot change the author of a comment.")
        
        # Proceed with the update
        return super().update(instance, validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'post_type', 'metadata', 'author', 'comments', 'created_at']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Post cannot be empty")
        return value

    def create(self, validated_data):
        return PostFactory.create_post(**validated_data)


    # # Override the serialization method to change the author field from a primary key to a username string
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['author'] = instance.author.username #UserSerializer(instance.author).data
    #     return response


    # Override the update method to add validation for allowable fields
    # def update(self, instance, validated_data):
    #     allowed_fields = ['content']
    #     for field in validated_data.keys():
    #         if field not in allowed_fields:
    #             raise ValidationError(f"Field {field} is not allowed")
    #
    #     for field, value in validated_data.items():
    #         if field in allowed_fields:
    #             setattr(instance, field, value)
    #
    #     instance.save()
    #     return instance

