from django import forms
from main.models import Post, Comment

# class PostForm(forms.Form):
#     author = forms.CharField(max_length=50, label='Автор', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     title = forms.CharField(min_length=5, max_length=100, label='Заголовок')
#     text = forms.CharField(widget=forms.Textarea, label='Текст поста')
#     image = forms.ImageField(required=False)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["author", "title", "text", "image"]

    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if author:
            self.fields['author'].initial = author
            #self.fields['author'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
            self.fields['author'].disabled = True


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

    # def __init__(self, *args, **kwargs):
    #
    #     pass
