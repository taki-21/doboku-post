from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions, generics, views, status, pagination, response
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Post, Category, Comment, Like
from .serializers import UserSerializer, CategorySerializer, PostSerializer, PostMiniSerializer, PostLikeSerializer, CommentSerializer, LikeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly

def Response_unauthorized():
    return Response({"detail": "権限がありません。"}, status.HTTP_401_UNAUTHORIZED)


class UserListCreateAPIView(generics.ListCreateAPIView):
    """カスタムユーザーモデルの取得（一覧）・登録APIクラス"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """カスタムユーザーモデルの取得（詳細）・更新APIクラス"""
    # permission_classes = [IsOwnerOrReadOnly]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def update(self, request, pk, *args, **kwargs):
        user = get_user_model().objects.get(id=pk)
        if request.user.id != user.id:
            return Response_unauthorized()
        response = super().update(request, pk, *args, **kwargs)

        return response

    def partial_update(self, request, pk, *args, **kwargs):
        user = get_user_model().objects.get(id=pk)
        if request.user.id != user.id:
            return Response_unauthorized()
        response = super().partial_update(request, pk, *args, **kwargs)

        return response

    def destroy(self, request, pk, *args, **kwargs):
        user = get_user_model().objects.get(id=pk)
        if request.user.id != user.id:
            return Response_unauthorized()
        response = super().destroy(request, pk, *args, **kwargs)
        return response


class CategoryListAPIView(generics.ListAPIView):
    """投稿モデルの取得（一覧）APIクラス"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='contains')
    published_at = filters.DateTimeFilter(lookup_expr='gt')

    order_by = filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('likes_count', 'likes_count'),
        ),
    )

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'category',
            'published_at',
            'prefecture',
            'order_by']


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
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostLikeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer


class PostMiniFilter(filters.FilterSet):

    class Meta:
        model = Post
        fields = ['author', ]


class PostMiniListAPIView(generics.ListAPIView):
    """投稿の位置モデルの取得（一覧）・投稿APIクラス"""
    queryset = Post.objects.all()
    serializer_class = PostMiniSerializer
    filter_class = PostMiniFilter


# class PostMiniRetrieveAPIView(generics.RetrieveAPIView):
#     """投稿の位置モデルの取得（詳細）・更新・削除APIクラス"""

#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


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
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



class LikeFilter(filters.FilterSet):
    class Meta:
        model = Like
        fields = ['author', 'post']


class LikeListCreateAPIView(generics.ListCreateAPIView):
    """いいねモデルの取得（一覧）・投稿APIクラス"""
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_class = LikeFilter
    pagination_class = StandardResultsSetPagination


class LikeDestroyAPIView(generics.DestroyAPIView):
    """いいねモデルの削除APIクラス"""
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Like.objects.all()
