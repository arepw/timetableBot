import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery = Celery('scrapper.tasks', include=['scrapper.tasks'])
celery.config_from_object('scrapper.celery_config')


# Celery Beat schedule
celery.conf.beat_schedule = {
    'get-screenshot-periodically': {
        'task': 'tasks.get_schedule',
        'schedule': float(os.getenv('UPDATE_RATE')),
    },
}

celery.autodiscover_tasks()
