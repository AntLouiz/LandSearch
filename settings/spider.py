from decouple import config

USGS_USERNAME = config('USGS_USERNAME')
USGS_PASSWORD = config('USGS_PASSWORD')
BASE_URL = 'https://earthexplorer.usgs.gov/'
HEADLESS = config('HEADLESS', default=True)
TEMP_DIR = '_temp/'
DOWNLOAD_DIR = config(
    'DOWNLOAD_DIR',
    default='downloads/'
)

BROKER_URL = config(
    'BROKER_URL'
)
