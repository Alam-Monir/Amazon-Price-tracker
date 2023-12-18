from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


base_url = "https://www.amazon.in/"
directory = 'Reports'
currency = 'Rs'
MIN_price = '10000'
MAX_price = '20000'
Name = "Mobile"
filters = {
    'min': MIN_price,
    'max': MAX_price,
}

def get_chrome_web_driver(options):
    return webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))

def get_web_driver_options():
    return webdriver.ChromeOptions()


def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')

def set_ignore_ssl_errors(options):
    options.add_argument('--ignore-ssl-errors')


def set_browser_as_incognito(options):
    options.add_argument('--incognito')


def set_automation_as_head_less(options):
    options.add_argument('--headless')

#options = webdriver.ChromeOptions()
#options.add_argument("--incognito")
#options.add_argument('--ignore-certificate-errors')
#options.add_argument('--ignore-ssl-errors')
#driver = webdriver.Chrome(options=options)