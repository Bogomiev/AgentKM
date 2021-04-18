from celery import shared_task
import random as r


@shared_task
def exchange_ut():
    print(f'Request: {r.random()}')
