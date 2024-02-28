import requests
from splinter import Browser
# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import matplotlib.pyplot as plt
import time


# a note to trigger git
def marketplace_search(name):
    # browser = Browser(driver_name='firefox', executable_path=ChromeDriverManager().install())
    browser = Browser(
        driver_name='chrome',
        service=Service()
    )

    base_url = 'https://www.facebook.com/marketplace/tampa/search?'
    parameters = {
        'min_price': 1000,
        'max_price': 30000,
        'days_listed': 7,
        'min_mileage': 50000,
        'max_mileage': 200000,
        'min_year': 2000,
        'max_year': 2007,
        'transmission': 'automatic',
        'make': 'honda',
        'model': 'civic'
    }
    parameters_list = []
    for (k, v) in parameters.items():
        parameters_list.append(f'{k}={v}')
    search_parameters = '&'.join(parameters_list)
    full_url = base_url + search_parameters
    print(full_url)

    browser.visit(full_url)
    browser.quit()

    #requests.put('https://www.facebook.com/marketplace/108288625865467/search/', )


def marketplace_selector(term):
    payload = {

    }
    requests.put('https://www.facebook.com/api/graphql/', payload)


if __name__ == '__main__':
    marketplace_selector('89119')
    marketplace_search('Hustlers')
