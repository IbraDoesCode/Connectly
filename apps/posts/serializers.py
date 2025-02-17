import os
from django.core.exceptions import ValidationError, PermissionDenied
from rest_framework import serializers
from PIL import Image
from io import BytesIO
from rest_framework import serializers
from .models import Post
from .factories import PostFactory, CommentFactory
from .models import Post, Comment
import ffmpeg

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
    image = serializers.ImageField(required=False)  
    video = serializers.FileField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'content', 'post_type', 'image', 'video', 'metadata', 'author', 'comments', 'created_at']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Post cannot be empty")
        return value
    
    def validate_video(file):
        # Check if the file's MIME type starts with 'video/'

        valid_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        if not file:
            raise ValidationError("No file was uploaded.")
        if not file.name:
            raise ValidationError("The uploaded file has no name.")
        filename, ext = os.path.splitext(file.name)
        if ext.lower() not in valid_extensions:
            raise ValidationError(f"This is not a valid video file. Please upload a video with one of the following extensions: {', '.join(valid_extensions)}.")
        if not file.content_type.startswith('video/'):
            raise ValidationError("This is not a valid video file. Please upload a video with a valid MIME type.")

    def create(self, validated_data):
        image = validated_data.get('image', None)
        video = validated_data.get('video', None)
        metadata = None

        # Automatically extract metadata if there's an image
        if image:
            metadata = self.extract_image_metadata(image)
            filename, ext = os.path.splitext(image.name)
            image.name = f"{metadata['width']}x{metadata['height']}_{filename}{ext}"

        # Automatically extract metadata if there's a video
        if video:
            metadata = self.extract_video_metadata(video)
            filename, ext = os.path.splitext(video.name)
            video.name = f"{metadata['width']}x{metadata['height']}_{metadata['duration']}s_{filename}{ext}"

        post_type = validated_data.get('post_type')
        if post_type == 'image' and metadata is None:
            raise serializers.ValidationError("Image posts require metadata")
        if post_type == 'video' and metadata is None:
            raise serializers.ValidationError("Video posts require metadata")

        if metadata is not None:
            validated_data['metadata'] = metadata
        
        return PostFactory.create_post(**validated_data)

    def extract_image_metadata(self, image_file):
        """Helper function to extract image metadata."""
        try:
            image = Image.open(image_file)
            width, height = image.size
            file_size = image_file.size
            file_type = None
            if image.format is not None:
                file_type = image.format  # JPEG, PNG, etc.
            return {
                'width': width,
                'height': height,
                'file_size': file_size,
                'file_type': file_type
            }
        except Exception as e:
            raise ValidationError(f"Error extracting image metadata: {str(e)}")

    def extract_video_metadata(self, video_file):
        """Helper function to extract video metadata."""
        try:
            probe = ffmpeg.probe(video_file, v='error', select_streams='v:0', show_entries='stream=width,height,duration')
            width = probe.get('streams', [{}])[0].get('width')
            height = probe.get('streams', [{}])[0].get('height')
            duration = probe.get('streams', [{}])[0].get('duration')
            file_size = video_file.size
            return {
                'width': width,
                'height': height,
                'duration': duration,
                'file_size': file_size,
            }
        except Exception as e:
            raise ValidationError(f"Error extracting video metadata: {str(e)}")



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

