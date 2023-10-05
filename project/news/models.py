from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, IntegerField
from django.db.models.functions import Coalesce
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta, datetime
import logging

logging.basicConfig(level=logging.DEBUG)

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
        post_rating = 0
        comments_rating = 0
        post_comments_rating = 0
        posts = Post.objects.filter(author=self)
        for p in posts:
            post_rating += p.rating
        comments = Comment.objects.filter(user=self.user)
        for c in comments:
            comments_rating += c.rating
        posts_comments = Comment.objects.filter(post__author=self)
        for pc in posts_comments:
            post_comments_rating += pc.rating

        print(post_rating)
        print('-------------')
        print(comments_rating)
        print('-------------')
        print(post_comments_rating)

        self.rating = post_rating * 3 + comments_rating + post_comments_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)

    def __str__(self):
        return self.category_name


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
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text_post) > 124:
            return self.text_post[:124] + '...'
        else:
            return self.text_post

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def send_subscription_emails(self):
        categories = self.post_category.all()
        subject = self.title_post

        for category in categories:
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                user_name = subscriber.username

                context = {'post': self, 'user': user_name}

                html_message = render_to_string('email_template.html', context)


                send_mail(
                    subject,
                    '',  # Оставляем пустым, так как текст письма будет в HTML
                    'boomer47@yandex.ru',
                    [subscriber.email],
                    html_message=html_message
                )






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
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')


class UserPostLimit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    post_count = models.IntegerField(default=0)


def send_weekly_news():
    print("send_weekly_news is running")
    logging.info("send_weekly_news started")
    # Найдем все посты (новости и статьи), опубликованные за последнюю неделю (7 дней назад от текущей даты)
    last_week = datetime.now() - timedelta(days=7)
    posts = Post.objects.filter(data_time__gte=last_week)

    # Получим список всех пользователей
    users = User.objects.all()

    for user in users:
        # Формируем сообщение для отправки
        subject = 'Еженедельная рассылка новостей'
        user_name = user.username
        context = {'posts': posts, 'user': user_name}

        # Используем render_to_string с вашим шаблоном 'weekly_newsletter.html'
        html_message = render_to_string('weekly_newsletter.html', context)

        # Отправляем письмо на почту пользователя
        send_mail(
            subject,
            '',  # Оставляем пустым, так как текст письма будет в HTML
            'boomer47@yandex.ru',  # Замените на свой email
            [user.email],
            html_message=html_message
        )

        logging.info('Отправлено письмо пользователю %s', user.username)

    logging.info("send_weekly_news completed")