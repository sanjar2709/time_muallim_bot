from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore

from tg.functions import send_post_to_channel


def start():
    scheduler = BlockingScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('cron', hour=5, minute=0, second=0, name='auto_check')
    def auto_check():
        send_post_to_channel()

    scheduler.start()
