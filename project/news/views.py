from datetime import datetime

from .models import Post

from django.views.generic import ListView, DetailView
# список всех новостей
class PostListView(ListView):
    queryset = Post.objects.order_by(
        '-created_at'
    )  # от новых к старым

    template_name = 'flatpages/news.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = 'Новости завтра!'
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/news_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'
