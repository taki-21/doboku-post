from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/<int:author_id>/', views.profile_edit, name='profile_edit'),
]
