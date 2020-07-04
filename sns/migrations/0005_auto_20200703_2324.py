# Generated by Django 3.0.3 on 2020-07-03 14:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sns', '0004_auto_20200703_2322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='good',
        ),
        migrations.AddField(
            model_name='post',
            name='good',
            field=models.ManyToManyField(blank=0, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]