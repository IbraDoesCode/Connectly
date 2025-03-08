from django.contrib.contenttypes.models import ContentType

from apps.medias.models import Media


class MediaFactory:
    @staticmethod
    def create_image(content_object, file, metadata=None):

        return Media.objects.create(
            media_type=Media.IMAGE,
            content_type=ContentType.objects.get_for_model(content_object),
            object_id=content_object.id,
            file=file,
            metadata=metadata,
        )

    @staticmethod
    def create_video(content_object, file, metadata=None):

        return Media.objects.create(
            media_type=Media.VIDEO,
            content_type=ContentType.objects.get_for_model(content_object),
            object_id=content_object.id,
            file=file,
            metadata=metadata,
        )