from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Post, Comment
from django.contrib.auth.hashers import make_password  # 追加


class UserSerializer(serializers.ModelSerializer):
    """ユーザー一覧シリアライザー"""
    class Meta:
        model = get_user_model()
        fields = '__all__'
        # read_only_fields = ('last_login', 'is_superuser', 'is_staff', 'is_active', 'first_name', 'last_name', 'date_joined', 'groups', 'user_permissions')

    def create(self, validated_data):
        password = validated_data.get('password', None)
        if password is not None:
            validated_data['password'] = make_password(password)
        return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     if 'password' in validated_data:
    #         instance.set_password(validated_data['password'])
    #     else:
    #         instance = super().update(instance, validated_data)
    #     instance.save()
    #     return instance


class CategorySerializer(serializers.ModelSerializer):
    """カテゴリ一覧シリアライザ"""
    class Meta:
        model = Category
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    # category = CategorySerializer()
    author = UserSerializer(read_only=True)
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
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all())
    author = UserSerializer(read_only=True)
    author_name = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), write_only=True)

    def create(self, validated_data):
        validated_data['author'] = validated_data.get('author_name', None)

        if validated_data['author'] is None:
            raise serializers.ValidationError('author not found.')

        del validated_data['author_name']

        return Comment.objects.create(**validated_data)

    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ('id', 'post', 'author', 'author_name', 'text', 'timestamp')
