from django.urls import path
from . import views

app_name = 'sns'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('reverse/', views.IndexReverseView.as_view(), name='index_reverse'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<str:category_slug>/',
         views.CategoryPostView.as_view(), name='category_post'),
    path('create/', views.form_view, name='form_view'),
    path('mypage/', views.MyPage.as_view(), name='my_page')
]
