import glob
import re
import os.path
from datetime import datetime
from settings import (
    BASE_URL as base_url,
    USGS_PASSWORD as password,
    USGS_USERNAME as username
)
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .config import profile, options
from .exceptions import ResultsNotFoundError


def make_login(client, credentials):
    input_username = client.find_element_by_xpath("//input[@id='username']")
    input_username.send_keys(credentials['username'])

    input_password = client.find_element_by_xpath("//input[@id='password']")
    input_password.send_keys(credentials['password'])

    client.find_element_by_xpath("//input[@id='loginButton']").click()


def download_image(order, client):
    try:
        acquisition_date = client.find_element_by_xpath(
            "(//td[@class='resultRowContent']//li[3])[1]"
        )

        regex = re.compile(r'(?<=\:).*')
        acquisition_date = re.search(regex, acquisition_date.text).group()
        order.raster.acquisition_date = datetime.strptime(
            acquisition_date,
            "%d-%b-%y"
        )
        order.raster.save()

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
    input_lat = client.find_element_by_xpath(
        "//div[@aria-describedby='coordEntryDialogArea']//input[@class='latitude txtbox decimalBox']"
    )

    input_long = client.find_element_by_xpath(
        "//div[@aria-describedby='coordEntryDialogArea']//input[@class='longitude txtbox decimalBox']"
    )

    client.implicitly_wait(1)

    input_lat.send_keys(
        str(latitude)
    )

    input_long.send_keys(
        str(longitude)
    )

    client.find_element_by_xpath(
        "//div[@id='coordEntryDialogArea']/..//span[text()='Add']"
    ).click()

    client.implicitly_wait(4)

    client.find_element_by_xpath(
        "//input[@value='Data Sets »']"
    ).click()

    client.implicitly_wait(4)

    client.find_element_by_xpath("//li[@id='cat_210']/div").click()

    client.find_element_by_xpath(
        "//span[@title='Landsat Collection 1 Standard Level-1 Scene Products']"
    ).click()

    client.find_element_by_xpath(
        "//input[@id='coll_12864']"
    ).click()

    client.find_element_by_xpath(
        "//form[@name='dataSetForm']//input[@value='Results »']"
    ).click()

    download_image(order, client)

    login_button = client.find_element_by_xpath("//input[@value='Login']")

    if login_button:
        login_button.click()
        make_login(client, credentials)
        download_image(order, client)

    download_button = client.find_element_by_xpath(
        "//*[@id='optionsPage']/div[1]/div[4]/input"
    )

    download_button.click()
