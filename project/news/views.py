from datetime import datetime
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm

# список всех новостей
class PostListView(ListView):
    queryset = Post.objects.order_by(
        '-created_at'
    )  # от новых к старым

    template_name = 'flatpages/news.html'
    context_object_name = 'posts'
    paginate_by= 6

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


class PostSearch(ListView):
    model = Post
    template_name = 'flatpages/news_search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# --- NEWS (тип = NEWS) ---
class NewsCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        # выставляем тип — новость
        post.type = Post.Type.NEWS
        return super().form_valid(form)


class NewsUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_form.html'

    def get_queryset(self):
        # разрешаем редактировать только объекты типа NEWS
        return Post.objects.filter(type=Post.Type.NEWS)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = Post.Type.NEWS  # гарантируем, что тип не изменится
        post.save()
        form.save_m2m()
        self.object = post
        return super().form_valid(form)

    def test_func(self):
        # только автор может редактировать (можно настроить иначе)
        obj = self.get_object()
        return obj.author.user == self.request.user


class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'flatpages/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type=Post.Type.NEWS)

    def test_func(self):
        obj = self.get_object()
        return obj.author.user == self.request.user


# --- ARTICLES (тип = ARTICLE) ---
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'flatpages/news_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        # чтобы показывались только статьи
        return Post.objects.filter(type=Post.Type.ARTICLE)


class ArticleCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = Post.Type.ARTICLE
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_form.html'

    def get_queryset(self):
        return Post.objects.filter(type=Post.Type.ARTICLE)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = Post.Type.ARTICLE
        post.save()
        form.save_m2m()
        self.object = post
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.author.user == self.request.user


class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'flatpages/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')  # или отдельный список статей
    def get_queryset(self):
        return Post.objects.filter(type=Post.Type.ARTICLE)
    def test_func(self):
        obj = self.get_object()
        return obj.author.user == self.request.user