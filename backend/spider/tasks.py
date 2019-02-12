from __future__ import absolute_import, unicode_literals
import glob
import os.path
import shutil
from datetime import datetime
from django.core import serializers
from backend.celery import app
from celery.utils.log import get_task_logger
from .decompressor import clean_file, check_zip_download_finished
from .spider import crawl
from .trimmer import crop_raster
from .uploader import get_shapefile, upload_file
from .config import temp_dir, profile


logger = get_task_logger(__name__)


@app.task()
def crawl_order(order):
    for order in serializers.deserialize('json', order):
        order = order.object
        order.status = 'executing'
        order.save()
        logger.info(order.id)

        # Set the profile download directory
        profile_download_dir = os.path.join(temp_dir, str(order.key))
        profile.set_preference('browser.download.dir', profile_download_dir)

        # Scraping the earthexplorer site
        crawl(order)

        # Check if the raster download is completed
        check_zip_download_finished(profile_download_dir)
        logger.info("Download finished.")

        downloaded_file = glob.glob("{}/*.zip".format(profile_download_dir))[0]

        # Downloading the shapefile
        get_shapefile(
            order.coordinates.shapefile.key,
            profile_download_dir
        )
        shapefile_dir = os.path.join(temp_dir, order.coordinates.shapefile.key)
        shapefile_path = glob.glob("{}/*.shp".format(profile_download_dir))[0]


        # Cleaning the .zip file to catch just the TIR raster
        logger.info("Cleaning the file.")
        clean_file(
            downloaded_file,
            profile_download_dir
        )

        upload_filename = "{}.tif".format(str(datetime.now()))
        upload_file_path = glob.glob("{}/*.tif".format(
            profile_download_dir
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

        shutil.rmtree(profile_download_dir)
