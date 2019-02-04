import glob
import os.path
from datetime import datetime
from django.core import serializers
from celery import Celery, group
from celery.utils.log import get_task_logger
from settings import BROKER_URL as broker_url
from .decompressor import clean_file, check_zip_download_finished
from .spider import crawl
from .trimmer import crop_raster
from .uploader import get_shapefile, upload_file
from .config import (
    download_dir,
    temp_dir,
    profile,
    options
)


app = Celery('tasks', broker=broker_url)
logger = get_task_logger(__name__)

@app.task
def download_shapefile_order(order):
    """
        A task to download a shapefile, using the *get_shapefile*
        function and returning the downloaded shapefile path.
    """
    for order in serializers.deserialize('json', order):
        order = order.object
        get_shapefile(
            order.coordinates.shapefile.key
        )
        shapefile_dir = os.path.join(temp_dir, order.coordinates.shapefile.key)
        shapefile_path = glob.glob("{}/*.shp".format(shapefile_dir))[0]

    return shapefile_path

@app.task
def download_raster_order(order):
    """
        A task to download the order raster file, using the
        *crawl* and *clean_file* functions to get just the TIR
        raster.
    """

    for order in serializers.deserialize('json', order):
        order = order.object
        profile_download_dir = os.path.join(temp_dir, str(order.key))
        profile.set_preference('browser.download.dir', profile_download_dir)

        # Scraping the earthexplorer site
        crawl(order)

        # Check if the raster download is completed
        check_zip_download_finished(profile_download_dir)
        logger.info("Download finished.")

        downloaded_file = glob.glob("{}/*.zip".format(profile_download_dir))[0]
        download_file_path = os.path.join(
            download_dir,
            str(datetime.now())
        )

        # Cleaning the .zip file to catch just the TIR raster
        logger.info("Cleaning the file.")
        clean_file(
            downloaded_file,
            download_file_path
        )
    return download_file_path


@app.task
def crawl_order(order):
    logger.info(order)

    # Set the profile download directory
    results = group([
        download_shapefile_order.s(order),
        download_raster_order.s(order)
    ])()
    results.get(100)
    print(results)
    """
    upload_filename = "{}.tif".format(str(datetime.now()))
    upload_file_path = glob.glob("{}/*.tif".format(
        download_file_path
    ))[0]

    # Cropping the raster with a shapefile
    logger.info("Cropping the raster.")
    crop_raster(
        upload_file_path,
        shapefile_path,
        upload_file_path
    )

    # Uploading the cropped raster result
    logger.info("Uploading the file.")
    upload_file(
        upload_filename,
        upload_file_path,
        order
    )

    # Mark as finished
    logger.info("Finished.")
    order.status = 'finished'
    order.save()
    """
