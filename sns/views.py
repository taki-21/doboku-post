from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post, Category
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IndexView(generic.ListView):
    model = Post
    template_name = 'sns/index.html'

    # def get_queryset(self):
    #     object_list = super().get_queryset()
    #     print(object_list)
    #     return Post.objects.filter(auther='admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class CategoryPostView(generic.ListView):
    model = Post
    template_name = 'sns/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        queryset = super().get_queryset().filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['category_list'] = Category.objects.all()
        return context
