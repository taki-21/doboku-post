from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    """ユーザー一覧シリアライザー"""
    class Meta:
        model = get_user_model()
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer):
    """カテゴリ一覧シリアライザ"""
    class Meta:
        model = Category
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
