from scrapper.celery_app import celery
from scrapper.schedule_scrapper import get_schedule_current


@celery.task(name='tasks.get_schedule')
def get_schedule():
    get_schedule_current()
