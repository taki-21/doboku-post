from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    age = models.IntegerField(null=True)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name



class Post(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    auther = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='')


    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
