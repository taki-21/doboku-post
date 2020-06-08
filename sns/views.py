from django.shortcuts import render
from django.views import generic
from .models import Post

# Create your views here.

class IndexView(generic.ListView):
    model = Post
    template_name = 'sns/index.html'
