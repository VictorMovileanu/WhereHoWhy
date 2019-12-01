from django import forms
from django_summernote.widgets import SummernoteWidget

from frontpage.models import Tweet, Post, Project


class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ['quote', 'source']


class ProjectForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'is_public', 'url', 'logo']
        model = Project


class PostForm(forms.ModelForm):
    summernote_fields = ['text']

    class Meta:
        model = Post
        fields = ['is_public', 'text']
        widgets = {
            'text': SummernoteWidget(),
        }
