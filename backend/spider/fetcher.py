from datetime import timedelta
from django.core import serializers
from backend.spider import tasks


def schedule_order(order):
    """
         Execute the task 'crawl_order' to a order
         with a date range.
    """
    interval = timedelta(16)
    crawl_date = order.raster.acquisition_date + interval
    order = serializers.serialize("json", [order])

    tasks.crawl_order.apply_async(
        args=[order],
        eta=crawl_date
    )
