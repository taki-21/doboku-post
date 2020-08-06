from django.db import models
from django.contrib.auth import get_user_model
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    author = models.ForeignKey(
        to=get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='upload/', null=True, blank=True)
    image_change = ImageSpecField(source='image',
                                  processors=[ResizeToFill(640, 480)],
                                  format='JPEG'
                                  )

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(to=Post, verbose_name='対象記事',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(to='self', verbose_name='親コメント',
                               null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.author} -  {self.text}'

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')
