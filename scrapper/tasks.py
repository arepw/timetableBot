from scrapper.celery_app import celery
from scrapper.schedule_scrapper import get_schedule_screenshots
from main import set_last_update_time


@celery.task(name='tasks.get_schedule')
def get_schedule():
    """ This task will run periodically. """
    # Run scrapper
    get_schedule_screenshots()
    # Set new last schedule update time
    set_last_update_time()
