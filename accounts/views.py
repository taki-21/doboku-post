from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate

from .forms import UserCreateForm, UserProfileForm

User = get_user_model()


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('sns:index')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


def profile_edit(request, author_id):
    author = get_object_or_404(get_user_model(), pk=author_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=author)
        print(form.errors)
        print(form.is_valid())
        if form.is_valid():
            print('セーブ前')
            form.save()
            print('セーブ後')
            return redirect('sns:my_page', pk=author.pk)
    else:
        form = UserProfileForm(instance=author)

    context = {
        'form': form,
        'author': author,
    }
    return render(request, 'registration/profile_edit.html', context)
