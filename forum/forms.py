from django import forms
from .models import Category


class PostForm(forms.Form):
    title = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    category = forms.ModelChoiceField(empty_label='Выберите категорию', label='Category',
                                      queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
