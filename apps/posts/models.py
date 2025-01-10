from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()
    DoesNotExist = models.ObjectDoesNotExist

    class Meta:
        abstract = True


# Create your models here.
class User(BaseModel):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Post(BaseModel):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]
