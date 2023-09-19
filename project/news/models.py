from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, IntegerField
from django.db.models.functions import Coalesce

article = 'AR'
news = 'NE'

choices = [
    (article, 'Cтатья'),
    (news, 'Новость'),
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author_post_rating = Post.objects.filter(author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rating') * 3, 0, output_field=IntegerField()))
        author_comment_rating = Comment.objects.filter(user_id=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating'), 0, output_field=IntegerField()))
        author_post_comment_rating = Comment.objects.filter(post__author__user=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating'), 0, output_field=IntegerField()))
        self.rating = author_post_rating['post_rating_sum'] + author_comment_rating['comments_rating_sum'] + \
                             author_post_comment_rating['comments_rating_sum']
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    type_post = models.CharField(max_length=10, choices=choices)
    data_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title_post = models.CharField(max_length=255)
    text_post = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        if len(self.text_post) > 124:
            return self.text_post[:124] + '...'
        else:
            return self.text_post


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    data_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1
