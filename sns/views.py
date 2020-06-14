from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from .models import Post, Category
from . import forms

# Create your views here.


class IndexView(generic.ListView):
    model = Post
    template_name = 'sns/index.html'

    # def get_queryset(self):
    #     condition = self.kwargs['condition']
    #     if condition == 0:
    #         queryset = Post.objects.all().order_by('-published_at')
    #     elif condition == 1:
    #         queryset = Post.objects.all().order_by('published_at')
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # conditionが指定されている場合
        condition = self.kwargs.get('condition')
        if condition == 0:
            context['object_list'] = Post.objects.all()
        elif condition == 1:
            context['object_list'] = Post.objects.all().reverse()

        #　conditionが指定されていない場合
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
        self.category = get_object_or_404(Category, slug=category_slug)
        self.queryset = super().get_queryset().filter(category=self.category)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # conditionが指定されている場合
        condition = self.kwargs.get('condition')
        if condition == 0:
            context['object_list'] = self.queryset
        elif condition == 1:
            context['object_list'] = self.queryset.order_by('published_at')

        context['category'] = self.category
        context['category_list'] = Category.objects.all()
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

def index_condition(request, condition):
    if condition == 0:
        object_list = Post.objects.all().order_by('-published_at')
    elif condition == 1:
        object_list = Post.objects.all().order_by('published_at')
    return TemplateResponse(request, 'sns/index.html', {'object_list': object_list})
