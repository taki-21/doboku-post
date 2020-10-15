from django.urls import path, include

from . import views


app_name = 'apiv1'
urlpatterns = [
    path('posts/', views.PostListCreateAPIView.as_view()),
    path('posts/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path('posts/mini/', views.PostMiniListAPIView.as_view()),
    path('posts/like/<int:pk>/', views.PostLikeRetrieveUpdateDestroyAPIView.as_view()),
    path('users/', views.UserListCreateAPIView.as_view()),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view()),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('comments/', views.CommentListCreateAPIView.as_view()),
    path('comments/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('likes/', views.LikeListCreateAPIView.as_view()),
    path('likes/<int:pk>/', views.LikeDestroyAPIView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
