import os.path
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from settings import BASE_DIR, TEMP_DIR


profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference(
    'browser.helperApps.neverAsk.saveToDisk',
    'application/zip'
)

temp_dir = os.path.join(BASE_DIR, TEMP_DIR)

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

options = Options()
options.set_headless(True)
