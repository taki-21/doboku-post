from django.urls import path
from .views import IndexView, CategoryPostView

app_name = 'sns'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<str:category_slug>/', CategoryPostView.as_view(), name='category_post'),
]
