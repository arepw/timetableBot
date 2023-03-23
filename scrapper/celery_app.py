from celery import Celery

celery = Celery('scrapper.tasks', include=['scrapper.tasks'])
celery.config_from_object('scrapper.celery_config')


# Celery Beat schedule
celery.conf.beat_schedule = {
    'get-screenshot-periodically': {
        'task': 'tasks.get_schedule',
        'schedule': 1800.0,
    },
}

celery.autodiscover_tasks()
