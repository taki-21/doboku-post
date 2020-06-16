from django import forms
from .models import Post, Comment, Reply

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = (
            'category',
            'title',
            'content',
            'image',
        )

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = (
            'author',
            'text'
        )


class ReplyForm(forms.ModelForm):
    class Meta():
        model = Reply
        fields = (
            'author',
            'text'
        )
