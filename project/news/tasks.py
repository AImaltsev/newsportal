from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post

def send_weekly_news():
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

        html_message = render_to_string('weekly_newsletter.html', context)

        # Отправляем письмо на почту пользователя
        send_mail(
            subject,
            '',  # Оставляем пустым, так как текст письма будет в HTML
            'boomer47@yandex.ru',  # Замените на свой email
            [user.email],
            html_message=html_message
        )