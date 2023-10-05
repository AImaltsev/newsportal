from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore
from news.models import send_weekly_news  # Импортируйте вашу функцию из models.py

class Command(BaseCommand):
    help = 'Starts the scheduler'

    def handle(self, *args, **options):
        # Создаем экземпляр планировщика
        scheduler = BackgroundScheduler()

        # Проверяем, есть ли уже хранилище "default" в планировщике
        if not scheduler.get_job("default"):
            # Если нет, то добавляем его
            scheduler.add_jobstore(DjangoJobStore(), "default")

        # Запускаем задачу с интервалом в 30 секунд
        scheduler.add_job(send_weekly_news, IntervalTrigger(seconds=30))

        # Запуск планировщика
        scheduler.start()

        try:

            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            # Обработка завершения работы планировщика
            scheduler.shutdown()
