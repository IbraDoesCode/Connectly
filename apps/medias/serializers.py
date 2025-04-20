import mimetypes

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from apps.medias.models import Media
from utils.media_compressor import MediaCompressor


class MediaSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True)
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(),
        write_only=True
    )
    object_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Media
        fields = ['id', 'file', 'content_type', 'object_id', 'url', 'media_type', 'metadata', 'uploaded_at']

    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return f"{settings.MEDIA_URL}{obj.file.url}"

    def validate(self, data):
        file = data.get('file')
        media_type = data.get('media_type')

        if not file:
            raise serializers.ValidationError('File field is required')

        mime_type, _ = mimetypes.guess_type(file.name)

        IMAGE_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
        VIDEO_MIME_TYPES = {'video/mp4', 'video/webm', 'video/ogg', 'video/mpeg'}

        if media_type == 'image':
            if mime_type not in IMAGE_MIME_TYPES:
                raise serializers.ValidationError(
                    f"Invalid file type for image. Allowed: {', '.join(IMAGE_MIME_TYPES)}")
        elif media_type == 'video':
            if mime_type not in VIDEO_MIME_TYPES:
                raise serializers.ValidationError(
                    f"Invalid file type for video. Allowed: {', '.join(VIDEO_MIME_TYPES)}")
        else:
            raise serializers.ValidationError("Unsupported media type. Use 'image' or 'video'.")

        return data


    def create(self, validated_data):
        file = validated_data.pop('file', None)
        if not file:
            raise serializers.ValidationError("File field is required")

        media_type = validated_data.get('media_type')

        if media_type == 'image':
            compressed_file = MediaCompressor.compress_image(file)
            metadata = MediaCompressor.extract_image_metadata(compressed_file)
        elif media_type == 'video':
            compressed_file = MediaCompressor.compress_video(file)
            metadata = MediaCompressor.extract_video_metadata(compressed_file)
        else:
            raise serializers.ValidationError('Unsupported media type')

        validated_data['file'] = compressed_file
        validated_data['metadata'] = metadata
        return super().create(validated_data)