from django.forms import ModelForm

from .models import Post

class PostForm(ModelForm):
    class Meta:
        # эта форма будет хранить данные в модели Book
        model = Post
        # на странице формы будут отображаться поля 'group' и 'text'
        fields = ['group', 'text']
