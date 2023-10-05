from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore
from news.models import send_weekly_news  # Импортируем функцию из models.py
import logging

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Создаем экземпляр планировщика
scheduler = BackgroundScheduler()

# Проверяем, есть ли уже хранилище "default" в планировщике
if not scheduler.get_jobstore("default"):
    # Если нет, то добавляем его
    scheduler.add_jobstore(DjangoJobStore(), "default")

# Настраиваем хранилище заданий
scheduler.add_jobstore(DjangoJobStore(), "default")

# Запускаем задачу с интервалом в 30 секунд
scheduler.add_job(send_weekly_news, IntervalTrigger(seconds=30))


# Определяем функцию для остановки планировщика при выключении сервера
def stop_scheduler():
    scheduler.shutdown()


if __name__ == '__main__':
    try:
        # Запуск планировщика
        scheduler.start()

        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        # Обработка завершения работы планировщика
        stop_scheduler()
