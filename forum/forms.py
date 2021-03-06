from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Posts


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя польхователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }


