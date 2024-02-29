import pickle

import requests
from selenium.webdriver import Keys
from splinter import Browser, Config
# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import matplotlib.pyplot as plt
import json
from urllib.parse import quote
import time
import os


def save_cookies(browser, filename):
    # Get the current cookies from the browser
    cookies = browser.driver.get_cookies()

    # Save the cookies to a file using pickle
    with open(filename, 'wb') as file:
        pickle.dump(cookies, file)


def load_cookies(browser, filename):
    # Load cookies from the file using pickle
    with open(filename, 'rb') as file:
        cookies = pickle.load(file)

    # Add the loaded cookies to the browser
    for cookie in cookies:
        browser.driver.add_cookie(cookie)


def login(browser):
    # Check saved cookies
    if os.path.exists('cookies.pkl'):
        # Load cookies from the file
        load_cookies(browser, 'cookies.pkl')

    login = browser.find_by_tag('form')
    if login:
        user = ''
        password = ''
        user_element = browser.find_by_id('email')
        if not user_element: exit(1)
        user_element.fill(user)

        pass_element = browser.find_by_id('pass')
        if not pass_element: exit(1)
        pass_element.fill(password)

        login_button = browser.find_by_css('button[name="login"]')

        if not login_button: exit(1)
        login_button.click()


        # Save cookies to a file
        time.sleep(0)
        save_cookies(browser, 'cookies.pkl')
        browser.visit('https://www.facebook.com/home.php')


def marketplace_search(search_term, marketplace_id):
    # Set Chrome options to disable notifications
    config = Config(
        fullscreen=False,
        headless=False
    )

    browser = Browser(
        driver_name='chrome',
        service=Service(),
        config=config,

    )

    base_url = f'https://www.facebook.com/marketplace/{marketplace_id}/search?'
    parameters = {
        'min_price': 1000,
        'max_price': 30000,
        'days_listed': 1,
        'query': search_term
    }
    parameters_list = []
    for (k, v) in parameters.items():
        parameters_list.append(f'{k}={v}')
    search_parameters = '&'.join(parameters_list) + '&exact=false'
    full_url = base_url + search_parameters
    print(full_url)

    browser.visit('https://www.facebook.com/')
    login(browser)

    # Simulate pressing the 'esc' key in the browser window
    browser.find_by_tag('body').type(Keys.ESCAPE)

    browser.visit(full_url)
    #browser.reload()

    browser.driver.type(Keys.RETURN)



    time.sleep(500)
    browser.quit()
