from django import forms
from main.models import Tweet


class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ['quote', 'source']
