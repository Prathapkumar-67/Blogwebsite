from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=254, unique=True)

    # You can add more fields here if needed
    def __str__(self):
        return self.username

class Post(models.Model):
    Post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='posts')
    category = models.CharField(max_length=50)
    images = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
