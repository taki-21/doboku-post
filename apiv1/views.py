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

from rest_framework import generics
from django.contrib.auth import get_user_model
from .models import Post, Category, Comment
from .serializers import UserSerializer, CategorySerializer, PostSerializer, CommentSerializer


class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
