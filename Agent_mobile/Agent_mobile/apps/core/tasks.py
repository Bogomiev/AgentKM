from celery import shared_task
from . exchange.trade import start_exchange


@shared_task
def exchange_trade():
    start_exchange()
