from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Post, Category, Comment
from . import forms


class IndexView(generic.ListView):
    model = Post
    template_name = 'sns/index.html'

    def get_queryset(self):
        q_word = self.request.GET.get('query')

        if q_word:
            object_list = Post.objects.filter(
                Q(title__icontains=q_word) |
                Q(author__username__icontains=q_word) |
                Q(content__icontains=q_word)
            )
        else:
            object_list = Post.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # conditionが指定されている場合
        condition = self.kwargs.get('condition')
        if condition == 0:
            context['object_list'] = Post.objects.all()
        elif condition == 1:
            context['object_list'] = Post.objects.all().reverse()

        # conditionが指定されていない場合
        context['category_list'] = Category.objects.all()
        return context


def post_detail(request, pk):
    """投稿詳細"""
    post = get_object_or_404(Post, pk=pk)

    # コメント機能
    comment_list = Comment.objects.filter(parent__isnull=True, post=post)

    # いいね機能
    liked = False
    if post.like.filter(id=request.user.id).exists():
        liked = True

    context = {
        'comment_list': comment_list,
        'post': post,
        'liked': liked,
    }

    if request.method == 'POST':
        form = forms.CommentForm(request.POST or None)
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('sns:post_detail', pk=post.pk)
    else:
        form = forms.CommentForm()

    context['form'] = form
    return render(request, 'sns/post_detail.html', context)


class CategoryPostView(generic.ListView):
    model = Post
    template_name = 'sns/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
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


def post_form(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('sns:index')
    else:
        form = forms.PostForm()
    return render(request, 'sns/post_form.html', {'form': form})


class MyPage(generic.TemplateView):
    model = Post
    template_name = 'sns/my_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.kwargs.get('pk')
        if user:
            context['user_post'] = Post.objects.filter(author=user)
            context['author'] = get_object_or_404(get_user_model(), pk=user)
        else:
            user = self.request.user
            context['user_post'] = Post.objects.filter(author=user)
            context['author'] = user
        return context


def post_remove(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.delete()
    return redirect('sns:my_page')


def post_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            print('セーブ前')
            form.save()
            print('セーブ後')
            return redirect('sns:my_page', )
    else:
        form = forms.PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'sns/post_form.html', context)


@login_required
def comment_create(request, post_pk):
    """記事へのコメント"""
    post = get_object_or_404(Post, pk=post_pk)
    form = forms.CommentForm(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('sns:comment_form', pk=post.pk)

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'sns/comment_form.html', context)


@login_required
def reply_create(request, comment_pk):
    """コメントへの返信"""
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    form = forms.CommentForm(request.POST or None)

    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.author = request.user
        reply.parent = comment
        reply.post = post
        reply.save()
        return redirect('sns:post_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }

    return render(request, 'sns/comment_form.html', context)


def comment_remove(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('sns:post_detail', pk=comment.post.pk)


def comment_edit(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    if request.method == 'POST':
        form = forms.CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('sns:post_detail', pk=post.pk)
    else:
        form = forms.CommentForm(instance=comment)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'sns/comment_form.html', context)


def like(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    print("request.POST.get('post_id'): ", request.POST.get('post_id'))
    print('post: ', post)
    print('post.like.count(): ', post.like.count())
    liked = False
    print('post.like.filter(id=request.user.id): ',
          post.like.filter(id=request.user.id))
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        liked = False
    else:
        post.like.add(request.user)
        liked = True
    # return redirect('sns:post_detail', pk=post.id)

    context = {
        'post': post,
        'liked': liked,
    }

    context_index = {
        'click_post': post,
    }
    print('click_post.id: ', post.id)
    render(request, 'sns/index.html', context_index)

    if request.is_ajax():
        html = render_to_string('sns/like.html', context, request=request)
        return JsonResponse({'form': html})
