from django.urls import path, include

from . import views


app_name = 'apiv1'
urlpatterns = [
    path('posts/', views.PostListCreateAPIView.as_view()),
    # path('posts/create/', views.PostCreateAPIView.as_view()),
    path('users/', views.UserListCreateAPIView.as_view()),
    path('users/<int:pk>/', views.UserRetrieveUpdate.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),


]


#     path('', views.IndexView.as_view(), name='index'),
#     path('<int:condition>/', views.IndexView.as_view(), name='index'),
#     path('detail/<int:pk>/', views.post_detail, name='post_detail'),
#     path('category/<str:category_slug>/',
#          views.CategoryPostView.as_view(), name='category_post'),
#     path('category/<str:category_slug>/<int:condition>',
#          views.CategoryPostView.as_view(), name='category_post'),
#     path('create/', views.post_form, name='form_view'),
#     path('my_page/', views.MyPage.as_view(), name='my_page'),
#     path('my_page/<int:pk>/', views.MyPage.as_view(), name='my_page'),
#     path('my_page/<int:post_pk>/remove/', views.post_remove, name='my_page_remove'),
#     path('my_page/<int:post_pk>/edit/', views.post_edit, name='my_page_edit'),
#     path('comment/<int:post_pk>/', views.comment_create, name='comment_create'),
#     path('reply/<int:comment_pk>/', views.reply_create, name='reply_create'),
#     path('comment/<int:comment_pk>/remove/', views.comment_remove, name='comment_remove'),
#     path('comment/<int:comment_pk>/edit/', views.comment_edit, name='comment_edit'),
#     path('like/', views.like, name='like'),
