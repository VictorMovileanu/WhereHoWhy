from django import forms
from WhereHoWhy.apps.main import Tweet


class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ['quote', 'source']
