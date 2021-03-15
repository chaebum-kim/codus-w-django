from django import forms
from django.core.validators import MaxLengthValidator
from .models import Article
import re


class ArticleForm(forms.Form):
    title = forms.CharField(label='Title', validators=[
                            MaxLengthValidator(100)])
    content = forms.CharField(label='Content', widget=forms.Textarea, validators=[
                              MaxLengthValidator(1000)])
    tag_set = forms.CharField(label='Tags', validators=[
                              MaxLengthValidator(100)], required=False)

    def clean_tag_set(self):
        data = self.cleaned_data.get('tag_set')
        if data:
            data = data.lower()
        return data
