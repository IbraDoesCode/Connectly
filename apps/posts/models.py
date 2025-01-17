from django.db import models
from ..users.models import User

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Post(BaseModel):
    liked_by = models.ManyToManyField(User, related_name='liked_posts')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"

class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return f"Comment by {self.author.username} on Post ID {self.post.id}"