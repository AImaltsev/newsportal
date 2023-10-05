import os
from datetime import timedelta
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['news'])  # Обновите имя приложения на "news"

# Включить повторные попытки подключения к брокеру при запуске
app.conf.broker_connection_retry_on_startup = True

# Расписание задач
app.conf.beat_schedule = {
    'send_weekly_newsletters': {
        'task': 'news.tasks.send_weekly_newsletters',
        'schedule': timedelta(weeks=1),  # Рассылка каждую неделю
    },
}