from django.forms import ModelForm
from django import forms
from .models import Blog, Comment


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'image' ]
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class CommentForm (ModelForm):

    class Meta:
        model = Comment
        fields = ['react','description']

        labels = {
            'description' : 'Add a comment',
        }
        def __init__(self, *args, **kwargs):
            super(CommentForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class':'input'})


