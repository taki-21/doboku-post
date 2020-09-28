from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions, generics, views, status, pagination, response
from django.contrib.auth import get_user_model
from .models import Post, Category, Comment, Like
from .serializers import UserSerializer, CategorySerializer, PostSerializer, PostMapSerializer, CommentSerializer, LikeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
# from django.db.models import Count


class UserListCreateAPIView(generics.ListCreateAPIView):
    """カスタムユーザーモデルの取得（一覧）・登録APIクラス"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """カスタムユーザーモデルの取得（詳細）・更新APIクラス"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class CategoryListAPIView(generics.ListAPIView):
    """投稿モデルの取得（一覧）APIクラス"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='contains')
    published_at = filters.DateTimeFilter(lookup_expr='gt')

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'category',
            'published_at',
            'prefecture', ]


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 12


class PostListCreateAPIView(generics.ListCreateAPIView):
    """投稿モデルの取得（一覧）・投稿APIクラス"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_class = PostFilter
    pagination_class = StandardResultsSetPagination


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """投稿モデルの取得（詳細）・更新・削除APIクラス"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostMapFilter(filters.FilterSet):

    class Meta:
        model = Post
        fields = ['author', ]


class PostMapListAPIView(generics.ListAPIView):
    """投稿の位置モデルの取得（一覧）・投稿APIクラス"""
    queryset = Post.objects.all()
    serializer_class = PostMapSerializer
    filter_class = PostMapFilter


class PostMapRetrieveAPIView(generics.RetrieveAPIView):
    """投稿の位置モデルの取得（詳細）・更新・削除APIクラス"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = [
            'post', ]


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """コメントモデルの取得（一覧）・投稿APIクラス"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_class = CommentFilter


class CommentRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView):
    """コメントモデルの取得（詳細）・更新・削除APIクラス"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeFilter(filters.FilterSet):
    class Meta:
        model = Like
        fields = ['user', 'post']


class LikeListCreateAPIView(generics.ListCreateAPIView):
    """いいねモデルの取得（一覧）・投稿APIクラス"""
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_class = LikeFilter
    pagination_class = StandardResultsSetPagination


class LikeDestroyAPIView(generics.DestroyAPIView):
    """いいねモデルの削除APIクラス"""
    queryset = Like.objects.all()
