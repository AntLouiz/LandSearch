import glob
import os.path
from datetime import datetime
from settings import BASE_URL as base_url
from settings import USGS_PASSWORD as password
from settings import USGS_USERNAME as username
from settings import TEMP_DIR
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .decompressor import clean_file, check_zip_download_finished
from .uploader import upload_file
from .trimmer import crop_raster
from .exceptions import ResultsNotFoundError
from .config import (
    download_dir,
    temp_dir,
    profile,
    options
)


def make_login(client, credentials):
    input_username = client.find_element_by_xpath("//input[@id='username']")
    input_username.send_keys(credentials['username'])

    input_password = client.find_element_by_xpath("//input[@id='password']")
    input_password.send_keys(credentials['password'])

    client.find_element_by_xpath("//input[@id='loginButton']").click()

    client.implicitly_wait(10)


def download_image(order, client):
    print(">>> Trying to download the image")
    try:
        client.find_element_by_xpath(
            "(//td[@class='resultRowContent']//a[@class='download'])[1]"
        ).click()

    except NoSuchElementException:
        order.status = 'no result'
        order.save()

        raise ResultsNotFoundError('No results found.')


def crawl(order):
    latitude = order.coordinates.latitude
    longitude = order.coordinates.longitude

    credentials = {
        'username': username,
        'password': password
    }

    client = webdriver.Firefox(firefox_profile=profile, options=options)

    response = client.get(base_url)

    coordinate_button = client.find_element_by_xpath("//div[@id='lat_lon_section']/label[2]")
    coordinate_button.click()


    client.find_element_by_xpath(
        "//input[@id='coordEntryAdd']"
    ).click()
    print(">>> Inserting the latitude and longitude.")
    input_lat = client.find_element_by_xpath(
        "//div[@aria-describedby='coordEntryDialogArea']//input[@class='latitude txtbox decimalBox']"
    )

    input_long = client.find_element_by_xpath(
        "//div[@aria-describedby='coordEntryDialogArea']//input[@class='longitude txtbox decimalBox']"
    )

    client.implicitly_wait(2)

    input_lat.send_keys(
        str(latitude)
    )

    input_long.send_keys(
        str(longitude)
    )

    client.find_element_by_xpath(
        "//div[@id='coordEntryDialogArea']/..//span[text()='Add']"
    ).click()

    client.implicitly_wait(2)
    print(">>> Searching the data set")
    client.find_element_by_xpath(
        "//input[@value='Data Sets »']"
    ).click()

    client.implicitly_wait(5)

    client.find_element_by_xpath("//li[@id='cat_210']/div").click()

    client.find_element_by_xpath(
        "//span[@title='Landsat Collection 1 Standard Level-1 Scene Products']"
    ).click()

    client.find_element_by_xpath(
        "//input[@id='coll_12864']"
    ).click()

    wait(client, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[9]/div[3]/div/button[1]"))).click()

    client.find_element_by_xpath(
        "//form[@name='dataSetForm']//input[@value='Results »']"
    ).click()

    download_image(order, client)

    login_button = client.find_element_by_xpath("//input[@value='Login']")

    if login_button:
        login_button.click()

        client.implicitly_wait(10)

        make_login(client, credentials)
        download_image(order, client)

    download_button = client.find_element_by_xpath(
        "//*[@id='optionsPage']/div[1]/div[4]/input"
    )

    download_button.click()
    print(">>> Downloading the image.")


def execute_scraping_order(order, shapefile_path):
    profile_download_dir = os.path.join(temp_dir, str(order.key))
    profile.set_preference('browser.download.dir', profile_download_dir)
    crawl(order)
    check_zip_download_finished(profile_download_dir)
    print(">>> Download finished.")

    downloaded_file = glob.glob("{}/*.zip".format(profile_download_dir))[0]
    download_file_path = os.path.join(
        download_dir,
        str(datetime.now())
    )

    print(">>> Cleaning the file.")
    clean_file(
        downloaded_file,
        download_file_path
    )

    upload_filename = "{}.tif".format(str(datetime.now()))
    upload_file_path = glob.glob("{}/*.tif".format(
        download_file_path
    ))[0]

    print(">>> Cropping the raster.")
    crop_raster(
        upload_file_path,
        shapefile_path,
        upload_file_path
    )

    print(">>> Uploading the file.")
    upload_file(
        upload_filename,
        upload_file_path,
        order
    )

    print(">>> Finished.")
