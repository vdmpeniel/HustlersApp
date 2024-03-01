import pickle
from functools import reduce
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


class Scrapper:
    get_details = False
    check_scammers = False
    facebook = 'https://www.facebook.com'
    preferences = {"profile.default_content_setting_values.notifications": 2}
    options = None
    driver = None

    def __init__(self, options):
        print('Initializing Scrapper...')
        self.get_details = options['get_details']
        self.check_scammers = options['check_scammers']

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--disable-notifications')

        if options['start_maximized']: self.options.add_argument('start-maximized')
        if options['is_headless']: self.options.add_argument('--headless')
        self.options.add_experimental_option("prefs", self.preferences)

        self.driver = webdriver.Chrome(options=self.options)

    def save_cookies(self, filename):
        # Get the current cookies from the browser
        cookies = self.driver.get_cookies()

        # Save the cookies to a file using pickle
        with open(filename, 'wb') as file:
            pickle.dump(cookies, file)

    def load_cookies(self, filename):
        # Load cookies from the file using pickle
        with open(filename, 'rb') as file:
            cookies = pickle.load(file)

        # Add the loaded cookies to the browser
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def do_login(self):
        self.driver.get('http:facebook.com')
        self.driver.implicitly_wait(1000)

        # Check saved cookies
        if os.path.exists('cookies.pkl'):
            # Load cookies from the file
            self.load_cookies('cookies.pkl')

        login = self.driver.find_element(By.TAG_NAME, 'form')
        if login:
            user =
            password =
            self.driver.find_element(By.ID, 'email').send_keys(user)
            self.driver.find_element(By.ID, 'pass').send_keys(password)
            self.driver.find_element(By.CSS_SELECTOR, 'button[name="login"]').click()
            # driver.implicitly_wait(5000)

            self.save_cookies('cookies.pkl')
            self.driver.get('https://www.facebook.com/home.php')

    def scroll_to_bottom(self):
        # scroll to the bottom
        last_height = 0
        new_height = 0
        attempt = 0
        total_scrolls = 0
        while attempt < 10 and total_scrolls < 100:
            # actual scroll
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
            # time.sleep(attempt / 3)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if last_height != new_height:
                total_scrolls = total_scrolls + 1
                attempt = 0
            else:
                attempt = attempt + 1

            # print(f'Attepmt: {attempt}')
            # print(f'Last: {last_height}')
            # print(f'New: {new_height}')
            # print(f'Total Scrolls: {total_scrolls}')
            # print()
            last_height = new_height

    def make_unique_list_in_place(self, list):
        # Remove duplicates while preserving the order
        unique_list = []
        seen_items = set()

        for item in list:
            if item not in seen_items:
                unique_list.append(item)
                seen_items.add(item)
        return unique_list

    def get_soup(self):
        # Parse the HTML content with BeautifulSoup
        html_content = self.driver.page_source
        return soup(html_content, 'html.parser')

    def get_field(self, field_name, list):
        result = ''
        for i in range(0, len(list) - 1):
            if list[i] == field_name:
                result = list[i + 1]
                break
        return result

    def get_posting_details(self, url):
        self.driver.get(url)
        dom = self.get_soup()
        images = dom.findAll('img')
        image_list = []
        for img in images:
            image_dict = {
                'src': img.get('src'),
                'alt': img.get('alt')
            }
            image_list.append(image_dict)
        span_list = dom.select('div[role="main"] span')
        span_text_list = list(map(lambda span: span.text, span_list))

        regex_list = [r'\d:\d{2}', r'(^\s?/\s?$)', r'\ufeff', r'\xa0', r'^\s?·\s?$', r'\n', '· In stock']
        span_text_list = [
            reduce(lambda s, regex: re.sub(regex, '', s), regex_list, input_string) for input_string in span_text_list
        ]
        span_text_list = list(map(lambda s: s.strip(' '), span_text_list))
        span_text_list = list(filter(lambda s: s not in ['', '/'], span_text_list))
        span_text_list = self.make_unique_list_in_place(span_text_list)

        title = span_text_list[0]
        price = span_text_list[1]

        location = span_text_list[3]
        condition = self.get_field('Condition', span_text_list)
        color = self.get_field('Color', span_text_list)
        brand = self.get_field('Brand', span_text_list)
        seller_name = self.get_field('Seller details', span_text_list)
        seller_joined = list(filter(lambda x: x.startswith('Joined Facebook in'), span_text_list))
        seller_joined = seller_joined[0] if len(seller_joined) >= 1 else ''
        description = dom.select('div.xz9dl7a.x4uap5.xsag5q8.xkhd6sd.x126k92a span')[0]

        posting_time = list(filter(lambda s: 'Listed' in s and 'ago' in s, span_text_list))
        posting_time = posting_time[0] if len(posting_time) >= 1 else ''
        posting_time = posting_time.split('in')[0].strip()
        return {
            'title': title,
            'price': price,
            'posting_time': posting_time,
            'location': location,
            'description': description.text,
            'condition': condition,
            'color': color,
            'brand': brand,
            'seller': {
                'name': seller_name,
                'url': '',
                'joined': seller_joined
            },
            'images': image_list
        }

    def capture_search_data(self):
        dom = self.get_soup()

        # print(beautiful_soup.prettify())
        search_results = dom.findAll('div', 'x3ct3a4')
        #search_results = search_results[:15]

        record_list = []
        for record in search_results:
            span_list = record.find_all('span')
            text_list = self.make_unique_list_in_place([span.text.strip() for span in span_list])
            url = f'{self.facebook}{record.find("a").get("href")}'
            image = record.find('img')
            record_data = {
                'title': text_list[1],
                'price': text_list[0],
                'location': text_list[2],
                'url': url,
                'main_image': {
                    'src': image.get('src'),
                    'alt': image.get('alt')
                },
                'details': self.get_posting_details(url) if self.get_details else {}
            }
            record_list.append(record_data)

        return {
            'count': len(record_list),
            'records': record_list
        }

    def marketplace_search(self, payload):
        start_time = time.time()
        self.do_login()
        base_url = f'{self.facebook}/marketplace/{payload["location_id"]}/search?'
        parameters = payload['parameters']
        parameters_list = []
        for (k, v) in parameters.items():
            parameters_list.append(f'{k}={v}')
        search_parameters = '&'.join(parameters_list) + '&exact=false'
        full_url = base_url + search_parameters

        self.driver.get(full_url)
        self.scroll_to_bottom()

        html_content = self.driver.page_source
        response = self.capture_search_data()
        end_time = time.time()
        response['execution_time'] = end_time - start_time
        self.driver.quit()

        for record in response['records']:
            print(record)
            print()
        print(response['execution_time'])

        print('DONE.')
        # time.sleep(100)
