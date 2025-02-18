import io
import os
import shutil
import tempfile
from django.core.exceptions import ValidationError

from django.core.files.base import ContentFile

from rest_framework import serializers
from PIL import Image
from rest_framework import serializers

from utils.media_compressor import MediaCompressor
from .models import CommentImage, Post, PostImage, PostVideo
from .factories import PostFactory, CommentFactory
from .models import Post, Comment
import ffmpeg

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source='post.id')
    # Add image field for upload (single image)
    image = serializers.ImageField(required=False)
    # For retrieving image url
    comment_image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'comment_type', 'created_at', 'image', 'comment_image']
        # extra_kwargs = {'post': {'read_only': True}, 'author': {'read_only': True}}

    def get_comment_image(self, obj):
        """Return the image data if it exists"""
        comment_image = obj.images.first() 
        if comment_image:
            return {
                "id": comment_image.id,
                "url": comment_image.image.url,
                "metadata": comment_image.metadata
            }
        return None
    
    def validate(self, data):
        """Validate comment data including image if present"""
        comment_type = data.get('comment_type')
        image = data.get('image')

        if comment_type == 'image' and not image:
            raise serializers.ValidationError("Image comments must include an image.")
        
        return data
        
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['author'] = instance.author.username if instance.author else None
    #     return response

    def create(self, validated_data):
        # Extract image data if it exists
        image = validated_data.pop('image', None)
        comment = None

        try:
            comment = CommentFactory.create_comment(**validated_data)

            # Process image if it exists
            if image:
                try:
                    # Compress the image with higher compression for comments
                    compressed_image = MediaCompressor.compress_image(
                        image,
                        quality=60,  # Higher compression (lower quality) for comments
                        max_width=800,  # Smaller max dimensions for comments
                        max_height=800
                    )
                    
                    # Extract image metadata
                    metadata = MediaCompressor.extract_image_metadata(compressed_image)

                    # Create the CommentImage instance
                    comment_image = CommentImage.objects.create(
                        comment=comment,
                        image=compressed_image,
                        metadata=metadata
                    )
                    
                    # Update the filename with metadata
                    ext = os.path.splitext(compressed_image.name)[1]
                    new_name = f"comment_{comment.id}_{comment_image.id}_{metadata['width']}x{metadata['height']}_{metadata['file_size']//1024}kb{ext}"
                    compressed_image.name = new_name
                    comment_image.image.save(new_name, compressed_image, save=True)
                    
                except Exception as img_exception:
                    raise serializers.ValidationError(f"Error processing comment image: {str(img_exception)}")

            return comment

        except Exception as e:
            if comment:
                comment.delete()
            raise serializers.ValidationError(f"Error creating comment: {str(e)}")

    def update(self, instance, validated_data):
        # Prevent changing post and author
        if instance.post != validated_data.get('post', instance.post):
            raise serializers.ValidationError("You cannot change the post of a comment.")
        
        if instance.author != validated_data.get('author', instance.author):
            raise serializers.ValidationError("You cannot change the author of a comment.")
        
        # Remove image from validated_data if present (images cannot be updated)
        validated_data.pop('image', None)
        
        return super().update(instance, validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    # For uploads
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    videos = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    # For retrieving media urls
    post_images = serializers.SerializerMethodField()
    post_videos = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'post_type', 'author', 'comments', 'created_at', 'images', 'videos', 'post_images', 'post_videos']

    def get_post_images(self, obj):
        return [{"id": image.id, "url": image.image.url, "metadata": image.metadata} for image in obj.images.all()]

    def get_post_videos(self, obj):
        return [{"id": video.id, "url": video.video.url, "metadata": video.metadata} for video in obj.videos.all()]
    
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
        ext = os.path.splitext(file.name)[1]
        if ext.lower() not in valid_extensions:
            raise ValidationError(f"This is not a valid video file. Please upload a video with one of the following extensions: {', '.join(valid_extensions)}.")
        if not file.content_type.startswith('video/'):
            raise ValidationError("This is not a valid video file. Please upload a video with a valid MIME type.")

    def validate(self, data):
        post_type = data.get('post_type')
        images = data.get('images', [])
        videos = data.get('videos', [])

        if post_type == 'image' and not images:
            raise serializers.ValidationError("Image posts must include at least one image.")
        if post_type == 'video' and not videos:
            raise serializers.ValidationError("Video posts must include at least one video.")

        return data
    
    def create(self, validated_data):
        images = validated_data.pop('images', [])
        videos = validated_data.pop('videos', [])
        post = None

        try:
            post = PostFactory.create_post(**validated_data)

            # Compress and save images
            for image in images:
                try:
                    # Compress the image
                    compressed_image  = MediaCompressor.compress_image(image)
                    
                    # Extract image metadata from the compressed image file
                    metadata = MediaCompressor.extract_image_metadata(compressed_image)

                    # Create the PostImage instance
                    post_image = PostImage.objects.create(
                        post=post,
                        image=compressed_image,
                        metadata=metadata
                    )
                    
                    # Update the filename with metadata
                    ext = os.path.splitext(compressed_image.name)[1]
                    new_name = f"{post.id}_{post_image.id}_{metadata['width']}x{metadata['height']}_{metadata['file_size']//1024}kb{ext}"
                    compressed_image.name = new_name
                    post_image.image.save(new_name, compressed_image, save=True)
                    
                except Exception as img_exception:
                    raise serializers.ValidationError(f"Error processing image: {str(img_exception)}")

            # Compress and save videos
            for video in videos:
                try:
                    # Compress the video
                    compressed_video = MediaCompressor.compress_video(video)
                    
                    # Extract video metadata
                    metadata = MediaCompressor.extract_video_metadata(compressed_video)
                    
                    # Create the PostVideo instance
                    post_video = PostVideo.objects.create(
                        post=post,
                        video=compressed_video,
                        metadata=metadata
                    )
                    # Update the filename with metadata
                    ext = os.path.splitext(compressed_video.name)[1]
                    new_name = f"{post.id}_{post_video.id}_{metadata['width']}x{metadata['height']}_{metadata['duration']}s_{metadata['file_size']//1024//1024}mb{ext}"
                    compressed_video.name = new_name
                    post_video.video.save(new_name, compressed_video, save=True)
                except Exception as vid_exception:
                    print(f"Video processing error: {str(vid_exception)}")
                    raise serializers.ValidationError(f"Error processing video: {str(vid_exception)}")
                
                # Validate the post
                post_type = validated_data.get('post_type')
                if post_type == 'image' and not images:
                    raise serializers.ValidationError("Image posts must include at least one image.")
                if post_type == 'video' and not videos:
                    raise serializers.ValidationError("Video posts must include at least one video.")
        except Exception as e:
            if post:
                post.delete()
            raise serializers.ValidationError(f"Error creating post: {str(e)}")
        return post
    
    @staticmethod
    def extract_image_metadata(image_file):
        """Helper function to extract image metadata."""
        try:
            if isinstance(image_file, ContentFile):
                image = Image.open(io.BytesIO(image_file.read()))
                file_size = image_file.size
            else:
                image = Image.open(image_file)
                file_size = getattr(image_file, 'size', 0)
                
            width, height = image.size
            file_type = image.format if image.format is not None else None
            
            return {
                'width': width,
                'height': height,
                'file_size': file_size,
                'file_type': file_type
            }
        except Exception as e:
            raise ValidationError(f"Error extracting image metadata: {str(e)}")

    @staticmethod
    def extract_video_metadata(video_file):
        """Helper function to extract video metadata."""
        try:
            # Create a temporary file to analyze with ffmpeg
            with tempfile.NamedTemporaryFile(suffix=os.path.splitext(video_file.name)[1], delete=False) as temp_file:
                if isinstance(video_file, ContentFile):
                    temp_file.write(video_file.read())
                    video_file.seek(0)  # Reset the file pointer
                else:
                    shutil.copyfileobj(video_file, temp_file)
                
                temp_file_path = temp_file.name
    
            try:
                # Probe the temporary file
                probe = ffmpeg.probe(temp_file_path, v='error', select_streams='v:0', show_entries='stream=width,height,duration')
                stream_info = probe.get('streams', [{}])[0]
                
                metadata = {
                    'width': int(stream_info.get('width', 0)),
                    'height': int(stream_info.get('height', 0)),
                    'duration': float(stream_info.get('duration', 0)),
                    'file_size': video_file.size if hasattr(video_file, 'size') else os.path.getsize(temp_file_path),
                }
    
                return metadata
    
            finally:
                # Clean up the temporary file
                os.unlink(temp_file_path)
    
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

