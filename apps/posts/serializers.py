
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import Post, Comment

from ..medias.models import Media
from ..medias.serializers import MediaSerializer
from ..users.serializers import ProfileBasicSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileBasicSerializer(source='author.profile', read_only=True)
    post = serializers.ReadOnlyField(source='post.id')
    media_files = serializers.FileField(write_only=True, required=False)
    media = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'comment_type', 'author', 'created_at', 'media', 'media_files', 'is_liked', 'like_count']

    def get_media(self, obj):
        media_queryset = Media.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id
        )
        request = self.context.get('request')
        
        if not media_queryset.exists():
            return []
        return MediaSerializer(media_queryset, context={'request': request}).data

    def get_is_liked(self, obj):
        if not self.context.get('request'):
            return False
        
        # Check if the comment is liked by the current user
        user = self.context.get('request').user
        return obj.liked_by.filter(id=user.id).exists()

    def get_like_count(self, obj):
        return obj.liked_by.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.comment_type == 'text':
            data.pop('media', None)

        return data

    def validate(self, data):
        comment_type = data.get('comment_type')
        content = data.get('content', '').strip()
        media_files = data.get('media_files', [])

        # Validate for empty content if the post type is text
        if comment_type == 'text' and not content:
            raise serializers.ValidationError("Text content cannot be empty.")

        if comment_type == 'image' and not media_files:
            raise serializers.ValidationError("An image is required.")

        if comment_type == 'video':
            raise serializers.ValidationError("Videos are not allowed in comments.")

        return data

    def create(self, validated_data):
        comment_type = validated_data.get('comment_type')
        media_file = validated_data.pop('media_files', [])
        comment = super().create(validated_data)

        if media_file:
            media_data = {
                'file': media_file,
                'media_type': comment_type,
                'content_type': ContentType.objects.get_for_model(comment).id,
                'object_id': comment.id
            }
            media_serializer = MediaSerializer(
                data=media_data
            )
            if media_serializer.is_valid():
                media_serializer.save()
            else:
                raise serializers.ValidationError(media_serializer.errors)

        return comment

    def update(self, instance, validated_data):
        # Prevent changing post and author
        if instance.post != validated_data.get('post', instance.post):
            raise serializers.ValidationError("You cannot change the post of a comment.")

        if instance.author != validated_data.get('author', instance.author):
            raise serializers.ValidationError("You cannot change the author of a comment.")

        # Remove image from validated_data if present (images cannot be updated)
        validated_data.pop('media', None)

        return super().update(instance, validated_data)


class PostFeedSerializer(serializers.ModelSerializer):
    author = ProfileBasicSerializer(source='author.profile', read_only=True)
    comments = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(source='liked_by.count', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'post_type', 'privacy_type', 'author', 'comments', 'comment_count', 'created_at', 'media',
                  'is_liked', 'like_count']

    def get_comments(self, obj):
        preview_comments = obj.comments.all()[:3]
        return CommentSerializer(preview_comments, many=True).data

    def get_media(self, obj):
        media_queryset = Media.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id
        )
        request = self.context.get('request')
        return MediaSerializer(media_queryset, many=True, context={'request': request}).data if media_queryset.exists() else []

    def get_is_liked(self, obj):
        request = self.context.get('request')
        return request and obj.liked_by.filter(id=request.user.id).exists()



class PostSerializer(serializers.ModelSerializer):
    author = ProfileBasicSerializer(source='author.profile', read_only=True)
    media_files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    media = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.IntegerField(source='liked_by.count', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'post_type', 'author', 'created_at', 'media', 'media_files', 'is_liked', 'like_count', 'comment_count', 'privacy_type']

    def get_media(self, obj):
        media_queryset = Media.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id
        )
        request = self.context.get('request')
        
        if not media_queryset.exists():
            return []
        return MediaSerializer(media_queryset, many=True, context={'request': request}).data

    def get_is_liked(self, obj):
        if not self.context.get('request'):
            return False
        
        # Check if the comment is liked by the current user
        user = self.context.get('request').user
        return obj.liked_by.filter(id=user.id).exists()

    def get_like_count(self, obj):
        return obj.liked_by.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.post_type == 'text':
            data.pop('media', None)

        return data

    def validate(self, data):
        post_type = data.get('post_type')
        content = data.get('content', '').strip()
        media_files = data.get('media_files', [])

        # Validate for empty content if the post type is text
        if post_type == 'text' and not content:
            raise serializers.ValidationError("Text content cannot be empty.")

        if post_type in ['image', 'video'] and not media_files:
            raise serializers.ValidationError("At least one media file is required.")

        return data

    def create(self, validated_data):
        post_type = validated_data.get('post_type')
        media_files = validated_data.pop('media_files', [])
        post = super().create(validated_data)

        for file in media_files:
            media_data = {
                'file': file,
                'media_type': post_type,
                'content_type': ContentType.objects.get_for_model(post).id,
                'object_id': post.id
            }
            media_serializer = MediaSerializer(
                data=media_data
            )
            if media_serializer.is_valid():
                media_serializer.save()
            else:
                raise serializers.ValidationError(media_serializer.errors)

        return post

    def update(self, instance, validated_data):
        # Prevent changing author
        if instance.author != validated_data.get('author', instance.author):
            raise serializers.ValidationError("You cannot change the author of a post.")

        # Remove media from validated_data if present (media cannot be updated)
        validated_data.pop('media', None)

        return super().update(instance, validated_data)
