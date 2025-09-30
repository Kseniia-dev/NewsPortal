import django_filters
from django_filters import FilterSet, ModelMultipleChoiceFilter
from .models import Post, Author
from django import forms


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )
    author = ModelMultipleChoiceFilter(
        field_name='author',
        label='Автор',
        queryset=Author.objects.all(),
        conjoined=False,
    )
    created_at = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Позже даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'created_at']