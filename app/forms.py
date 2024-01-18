from django import forms

from django.db import models

class PostForm(forms.Form):
    title = forms.CharField(max_length=30, label='タイトル')
    content = forms.CharField(label='本文', widget=forms.Textarea())

class PostReview(forms.Form):
    title = forms.CharField(label='タイトル', max_length=200)
    content = forms.CharField(label='本文', widget=forms.Textarea())