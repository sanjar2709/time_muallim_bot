from celery import shared_task
from .models import Users


@shared_task
def test():
    print(f"Hello world many to many  all function")
    return True
