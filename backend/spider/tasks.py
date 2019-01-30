import glob
import os.path
from django.core import serializers
from .config import temp_dir
from celery import Celery
from celery.utils.log import get_task_logger
from .spider import execute_scraping_order
from .uploader import get_shapefile
from settings import BROKER_URL as broker_url


app = Celery('tasks', broker=broker_url)
logger = get_task_logger(__name__)


@app.task
def crawl_order(order):
    for order in serializers.deserialize('json', order):
        order = order.object
        logger.info(order.id)

        get_shapefile(
            order.coordinates.shapefile.key
        )
        shapefile_dir = os.path.join(temp_dir, order.coordinates.shapefile.key)
        shapefile_path = glob.glob("{}/*.shp".format(shapefile_dir))[0]

        execute_scraping_order(
            order,
            shapefile_path
        )

        order.status = 'finished'
        order.save()
