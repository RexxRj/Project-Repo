from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['post']
        labels = {
            'user_name': 'Name',
            'user_email': 'Email',
            'text': 'Comment'
        }