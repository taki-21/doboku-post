from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions, generics, views, status
# from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Post, Category, Comment, Like
from .serializers import UserSerializer, CategorySerializer, PostSerializer, CommentSerializer, LikeSerializer
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

    # order_by = filters.OrderingFilter(
    #     fields=(
    #         ('published_at', 'published_at'),
    #     ),
    # )

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'category',
            'published_at',
            'prefecture', ]


class PostListCreateAPIView(generics.ListCreateAPIView):
    """投稿モデルの取得（一覧）・投稿APIクラス"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_class = PostFilter

    # def get_queryset(self):
    #     queryset = Post.objects.all()
    #     ordering = self.request.query_params.get('like_post', None)
    #     if ordering is not None:
    #         queryset = queryset.
    # filter_backends = (DjangoFilterBackend, OrderingFilter,)
    # filter_fields = 'likes_count'
    # ordering_fields = '__all__'
    # ordering_fields = ('number_of_likes',)
    # ordering_fields = '__all__'
    # ordering = ('number_of_likes',)

    # #認証済のみアクセス可能
    # permission_classes = [IsAuthenticated]


# class PostCreateAPIView(generics.CreateAPIView):
#     """投稿モデルの登録APIクラス"""
#     serializer_class = PostSerializer


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """投稿モデルの取得（詳細）・更新・削除APIクラス"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """コメントモデルの取得（一覧）・投稿APIクラス"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


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


class LikeDestroyAPIView(generics.DestroyAPIView):
    """いいねモデルの削除APIクラス"""
    queryset = Like.objects.all()
