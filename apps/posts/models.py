from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User # Reference djano's built-in User model

from apps.medias.models import Media


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        
class Post(BaseModel):
    POST_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video')
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text')
    liked_by = models.ManyToManyField(User, related_name='liked_posts')

    def clean(self):
        media = Media.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)
        image_count = media.filter(media_type=Media.IMAGE).count()
        video_count = media.filter(media_type=Media.VIDEO).count()

        if video_count > 1:
            raise ValidationError('Only one video allowed')
        if image_count > 20:
            raise ValidationError('Only 20 images allowed')


    def save(self, *args, **kwargs):
        # Prevent changing the author if the post already exists
        if self.pk:
            original = Post.objects.get(pk=self.pk)
            if self.author != original.author:
                raise ValidationError("You cannot change the author of a post.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"


class Comment(BaseModel):
    COMMENT_TYPES = [
        ('text', 'Text'),
        ('image', 'Image')
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=True)
    comment_type = models.CharField(max_length=10, choices=COMMENT_TYPES, default='text')
    liked_by = models.ManyToManyField(User, related_name='liked_comments')

    def clean(self):
        media = Media.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)

        if media.count() > 1:
            raise ValidationError("A comment can have only one media file (image).")

    def save(self, *args, **kwargs):
        # Prevent changing post if the comment already exists
        if self.pk:
            original = Comment.objects.get(pk=self.pk)
            if self.post != original.post:
                raise ValidationError("You cannot change the post of a comment.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.author.username} on Post ID {self.post.id}"
