from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category
from . import forms

# Create your views here.


class IndexView(generic.ListView):
    model = Post
    template_name = 'sns/index.html'

    # def get_queryset(self):
    #     object_list = super().get_queryset()
    #     print(object_list)
    #     return Post.objects.filter(author='admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'sns/post_detail.html'



class CategoryPostView(generic.ListView):
    model = Post
    template_name = 'sns/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        print('category_slug: ', category_slug)
        self.category = get_object_or_404(Category, slug=category_slug)
        print('self.category: ', self.category)
        queryset = super().get_queryset()
        print('queryset1: ', queryset)
        queryset = super().get_queryset().filter(category=self.category)
        print('queryset2: ', queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('context1: ', context)
        context['category'] = self.category
        print('context2: ', context)
        context['category_list'] = Category.objects.all()
        print('context3: ', context)
        return context


def form_view(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('sns:index')
    else:
       form = forms.PostForm()
    return render(request, 'sns/form_view.html', {'form': form})

class MyPage(generic.TemplateView):
    model = Post
    template_name = 'sns/my_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login_user = self.request.user
        print('login_user: ', login_user)
        context['user_post'] = Post.objects.filter(author=login_user)
        print(context)
        return context
