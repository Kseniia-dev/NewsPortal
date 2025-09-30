from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # не включаем поля author, type, rating, created_at
        fields = ['author', 'title', 'text', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }