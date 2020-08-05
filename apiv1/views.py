# from django.shortcuts import render, get_object_or_404, redirect
# from django.views import generic
# from django.contrib.auth import get_user_model
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.db.models import Q
# from django.template.loader import render_to_string
# from django.http import JsonResponse
# from django.db.models import Count
# from .models import Post, Category, Comment
# from . import forms

from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions, generics, views, status
# from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Post, Category, Comment, Like
from .serializers import UserSerializer, CategorySerializer, PostSerializer, CommentSerializer, LikeSerializer
from django_filters import rest_framework as filters
from django.db.models import Count


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
        fields = ['title', 'category', 'published_at']


class PostListCreateAPIView(generics.ListCreateAPIView):
    """投稿モデルの取得（一覧）・投稿APIクラス"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_class = PostFilter


# class PostCreateAPIView(generics.CreateAPIView):
#     """投稿モデルの登録APIクラス"""
#     serializer_class = PostSerializer


class PostRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """コメントモデルの取得（一覧）・投稿APIクラス"""
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

