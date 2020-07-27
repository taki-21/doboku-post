from django import forms
from .models import Post, Comment
from .widgets import FileInputWithPreview


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'category',
            'title',
            'content',
            'image',
        )
        widgets = {
            # 'image': FileInputWithPreview,
            # 次のようにすると、プレビューエレメントがウィジェットに含まれない。つまりプレビューエレメントを自分で好きな場所にかける
            'image': FileInputWithPreview(include_preview=False),
        }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = (
            'text',
        )
