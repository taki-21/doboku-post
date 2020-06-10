from django.urls import path
from . import views

app_name = 'sns'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<str:category_slug>/',
         views.CategoryPostView.as_view(), name='category_post'),
    path('create/', views.form_view, name='form_view')
]
