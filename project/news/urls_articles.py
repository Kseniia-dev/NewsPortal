from django.urls import path
from .views import ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='article_create'),         # /articles/create/
path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),    # /articles/5/edit/
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]