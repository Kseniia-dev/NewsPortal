from django.urls import path
from .views import PostListView, PostDetail
from django.views.generic import TemplateView

urlpatterns = [
    path('', PostListView.as_view(), name='news'),
    path('<int:pk>/', PostDetail.as_view(), name='news_detail'),
    path('', TemplateView.as_view(template_name='flatpages/default.html'), name='home'),
]
