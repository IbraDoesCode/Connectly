import cloudinary
from cloudinary.utils import cloudinary_url
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from apps.medias.models import Media


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
        fields = ['id', 'file', 'content_type', 'object_id', 'url', 'media_type', 'uploaded_at']

    def get_url(self, obj):
        public_id = getattr(obj.file, 'public_id', str(obj.file))
        url, _ = cloudinary_url(public_id, resource_type='video' if obj.media_type == 'video' else 'image', secure=True)
        return url
    
    def validate(self, data):
        if not data.get('file'):
            raise ValidationError('File field is required')
        return data
        
    def create(self, validated_data):
        file = validated_data.pop('file', None)
        media_type = validated_data.get('media_type')

        if not file:
            raise ValidationError('File field is required')
        
        upload_options = {
            'resource_type': 'video' if media_type == 'video' else 'image'
        }
        
        result = cloudinary.uploader.upload(file, **upload_options)

        validated_data['file'] = result['public_id']
        return Media.objects.create(**validated_data)

