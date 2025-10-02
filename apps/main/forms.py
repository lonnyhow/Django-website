# title, short_description, full_description, image, category

from django import forms

from .models import Article, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'your comment...'
            })
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'short_description', 'full_description', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            })
        }