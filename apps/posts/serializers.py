from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']
        extra_kwargs = {'post': {'read_only': True}}

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments']

    # Override the serialization method to change the author field from a primary key to a username string
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['author'] = instance.author.username #UserSerializer(instance.author).data
        return response

    # Override the update method to add validation for allowable fields
    def update(self, instance, validated_data):
        allowed_fields = ['content']
        for field in validated_data.keys():
            if field not in allowed_fields:
                raise ValidationError(f"Field {field} is not allowed")

        for field, value in validated_data.items():
            if field in allowed_fields:
                setattr(instance, field, value)

        instance.save()
        return instance
