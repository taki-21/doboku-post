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
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    author = UserSerializer()
    author_name = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), write_only=True)
    like_count = serializers.IntegerField(
        source='like.count',
        read_only=True
    )
    image_change = serializers.ImageField(read_only=True)

    def create(self, validated_data):
        validated_data['author'] = validated_data.get('author_name', None)

        if validated_data['author'] is None:
            raise serializers.ValidationError('author not found.')

        del validated_data['author_name']

        return Post.objects.create(**validated_data)

    class Meta:
        model = Post
        fields = ('id', 'category', 'author', 'author_name', 'title', 'content',
                  'published_at', 'image', 'image_change', 'like', 'like_count')
        # fields = '__all__'
        read_only_fields = ('like',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ('id', 'post', 'author', 'timestamp')
