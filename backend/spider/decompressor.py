import zipfile
import glob
import os
import time
import shutil
from .exceptions import TimeoutError


def clean_dir(dir_path):
    shutil.rmtree(dir_path)
    os.mkdir(dir_path)


def decompress_zip_file(file_path, output_dir='./'):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


def clean_file(file_path, output_dir='./'):
    decompress_zip_file(file_path, output_dir)

    tir_file = glob.glob("{}/*TIR.tif".format(output_dir))
    all_files = glob.glob("{}/*.tif".format(output_dir))

    files_to_exclude = [file for file in all_files if file not in tir_file]

    for file in files_to_exclude:
        os.remove(file)


def check_zip_download_finished(download_dir):
    waiting_seconds = 0
    download_finished = False

    time.sleep(waiting_seconds)

    while not download_finished:
        time.sleep(1)
        try:
            glob.glob("{}/*.zip.part".format(download_dir))[0]
            download_finished = False

        except IndexError:
            download_finished = True

    if not download_finished:
        raise TimeoutError('The download is not finished.')

    time.sleep(waiting_seconds)

    return download_finished
