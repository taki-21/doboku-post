from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from apiv1.widgets import FileInputWithPreview
from django import forms

User = get_user_model()


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        if User.USERNAME_FIELD == 'email':
            fields = ('email',)
        else:
            fields = ('username', 'email')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'icon_image', 'introduction', 'email')
        widgets = {
            # 'image': FileInputWithPreview,
            # 次のようにすると、プレビューエレメントがウィジェットに含まれない。つまりプレビューエレメントを自分で好きな場所にかける
            'icon_image': FileInputWithPreview(include_preview=False),
        }
