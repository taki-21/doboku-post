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
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Post, Category, Comment
from .serializers import UserSerializer, CategorySerializer, PostSerializer, CommentSerializer

from django.db.models import Count


class UserListCreateAPIView(generics.ListCreateAPIView):
    """カスタムユーザーモデルの取得（一覧）・登録APIクラス"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetail(views.APIView):

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=pk)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status.HTTP_200_OK)

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    """投稿モデルの取得（一覧）・投稿APIクラス"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# class PostCreateAPIView(generics.CreateAPIView):
#     """投稿モデルの登録APIクラス"""
#     serializer_class = PostSerializer


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
