from django.core import serializers
from backend.celery import app
from backend.core.models import ScrapingOrder
from backend.spider.tasks import crawl_order


@app.task()
def check_orders():
    orders = ScrapingOrder.objects.filter(
        status='Waiting',
        is_active=True
    ).all()

    for order in orders:
        order = serializers.serialize("json", [order])
        crawl_order.delay(order)


app.conf.beat_schedule = {
    "check-orders": {
        "task": "backend.core.tasks.check_orders",
        "schedule": 60.0
    }
}
