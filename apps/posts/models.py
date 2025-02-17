from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User # Reference djano's built-in User model

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
    content = models.TextField(blank=False)
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text')
    metadata = models.JSONField(null=True, blank=True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts')
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)

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
    content = models.TextField(blank=False)
    comment_type = models.CharField(max_length=10, choices=COMMENT_TYPES, default='text')
    metadata = models.JSONField(null=True, blank=True)
    liked_by = models.ManyToManyField(User, related_name='liked_comments')
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Prevent changing post if the comment already exists
        if self.pk:
            original = Comment.objects.get(pk=self.pk)
            if self.post != original.post:
                raise ValidationError("You cannot change the post of a comment.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.author.username} on Post ID {self.post.id}"