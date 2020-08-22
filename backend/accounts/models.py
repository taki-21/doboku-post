from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


def get_icon_image_path(instance, filename):
    return 'images/{0}/icon_image/{1}'.format(instance, filename)


def get_home_image_path(instance, filename):
    return 'images/{0}/home_image/{1}'.format(instance, filename)


class CustomUser(AbstractUser):
    """カスタムユーザーモデル"""
    email = models.EmailField(
        verbose_name='メールアドレス',
        unique=True
    )
    username = models.CharField(
        verbose_name='ユーザ名',
        unique=True,
        max_length=20
    )
    introduction = models.TextField(
        verbose_name='自己紹介',
        max_length=150,
        blank=True, null=True
    )
    icon_image = models.ImageField(
        verbose_name='アイコン画像',
        blank=True,
        null=True,
        default='images/custom_user/icon_image/default_icon.png',
        upload_to=get_icon_image_path
    )
    home_image = models.ImageField(
        verbose_name='ホーム画像',
        blank=True, null=True,
        default='images/custom_user/home_image/home.png',
        upload_to=get_home_image_path
    )

    # def __str__(self):
    #     return self.username
