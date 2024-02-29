import pickle

import requests
from selenium import webdriver
from selenium.webdriver import Keys
from splinter import Browser, Config
# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import matplotlib.pyplot as plt
import json
from urllib.parse import quote
import time
import os


def save_cookies(driver, filename):
    # Get the current cookies from the browser
    cookies = driver.get_cookies()

    # Save the cookies to a file using pickle
    with open(filename, 'wb') as file:
        pickle.dump(cookies, file)


def load_cookies(driver, filename):
    # Load cookies from the file using pickle
    with open(filename, 'rb') as file:
        cookies = pickle.load(file)

    # Add the loaded cookies to the browser
    for cookie in cookies:
        driver.add_cookie(cookie)


def do_login(driver):
    driver.get('http:facebook.com')
    driver.implicitly_wait(1000)

    # Check saved cookies
    if os.path.exists('cookies.pkl'):
        # Load cookies from the file
        load_cookies(driver, 'cookies.pkl')

    login = driver.find_element(By.TAG_NAME, 'form')
    if login:
        user =
        password =
        driver.find_element(By.ID, 'email').send_keys(user)
        driver.find_element(By.ID, 'pass').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'button[name="login"]').click()
        driver.implicitly_wait(5000)

        save_cookies(driver, 'cookies.pkl')
        driver.get('https://www.facebook.com/home.php')


def scroll_to_bottom(driver):
    # scroll to the bottom
    last_height = 0
    new_height = 0
    attempt = 0
    total_scrolls = 0
    while attempt < 10 and total_scrolls < 100:
        # actual scroll
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(attempt / 3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if last_height != new_height:
            total_scrolls = total_scrolls + 1
            attempt = 0
        else:
            attempt = attempt + 1

        print(f'Attepmt: {attempt}')
        print(f'Last: {last_height}')
        print(f'New: {new_height}')
        print(f'Total Scrolls: {total_scrolls}')
        print()
        last_height = new_height


def marketplace_search(payload):
    preferences = {"profile.default_content_setting_values.notifications": 2}
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", preferences)
    options.add_argument("start-maximized")
    options.add_argument('start-maximized')
    options.add_argument('--disable-notifications')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    do_login(driver)
    base_url = f'https://www.facebook.com/marketplace/{payload["location_id"]}/search?'
    parameters = payload['parameters']
    parameters_list = []
    for (k, v) in parameters.items():
        parameters_list.append(f'{k}={v}')
    search_parameters = '&'.join(parameters_list) + '&exact=false'
    full_url = base_url + search_parameters
    print(full_url)

    driver.get(full_url)
    scroll_to_bottom(driver)

    print('DONE.')
    time.sleep(100)
    driver.quit()
