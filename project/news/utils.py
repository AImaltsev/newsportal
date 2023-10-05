from django.core.mail import send_mail

def send_weekly_news_to_user(user, articles):
    subject = "Еженедельная рассылка новостей"
    message = "Вот какие новости у нас есть за неделю:"
    for article in articles:
        message += f"\n\nДата: {article.data_time.strftime('%Y-%m-%d')}\nЗаголовок: {article.title_post}\nОписание: {article.text_post[:50]}...\nСсылка: {article.get_absolute_url()}"

    send_mail(subject, message, "boomer47@yandex.ru", [user.email])