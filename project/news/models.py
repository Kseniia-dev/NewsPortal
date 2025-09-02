from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.
class Author (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"Author<{self.user.username}> (rating={self.rating})"

    def update_rating(self):
        # 1) суммарный рейтинг статей автора * 3
        posts_total = self.posts.aggregate(total=Sum('rating'))['total'] or 0
        # 2) суммарный рейтинг всех комментариев автора
        author_comments_total = self.user.comments.aggregate(total=Sum('rating'))['total'] or 0
        # 3) суммарный рейтинг всех комментариев к статьям автора
        comments_to_posts_total = Comment.objects.filter(post__author=self).aggregate(total=Sum('rating'))['total'] or 0

        self.rating = posts_total * 3 + author_comments_total + comments_to_posts_total
        self.save(update_fields=['rating'])

class Category (models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post (models.Model):
    class Type (models.TextChoices):
        ARTICLE = 'AR', 'Статья'
        NEWS = 'NW', 'Новость'

    name = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='posts')
    type = models.CharField(max_length=2, choices=Type.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    # many-to-many через промежуточную модель
    categories = models.ManyToManyField('Category', through='PostCategory', related_name='posts')

    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_type_display()}: {self.title} (rating={self.rating})"

    # методы like/dislike
    def like(self):
        self.rating += 1
        self.save(update_fields=['rating'])

    def dislike(self):
        self.rating -= 1
        self.save(update_fields=['rating'])

    # превью первых 124 символов + «…»
    def preview(self):
        return (self.text[:124] + '...') if len(self.text) > 124 else self.text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts')

    def __str__(self):
        return f"{self.post.title} — {self.category.name}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title} (rating={self.rating})"

    def like(self):
        self.rating += 1
        self.save(update_fields=['rating'])

    def dislike(self):
        self.rating -= 1
        self.save(update_fields=['rating'])