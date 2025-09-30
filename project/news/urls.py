from django.urls import path
from .views import (
    PostListView, PostDetail, PostSearch,
    NewsCreateView, NewsUpdateView, NewsDeleteView
)
from django.views.generic import TemplateView

urlpatterns = [
    path('', PostListView.as_view(), name='news_list'),
    path('<int:pk>/', PostDetail.as_view(), name='news_detail'),
    path('search/', PostSearch.as_view(), name='news_search'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
]
