import os
import pickle

import requests
from selenium.webdriver import Keys
from splinter import Browser
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
import scrapping_splinter
import scrapping_selenium
import facebook_graphql
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/api/greet', methods=['POST'])
def greet():
    return 'Hello World!'


@app.route('/api/search', methods=['POST'])
def run_search():
    facebook = facebook_graphql.GraphQL()
    location_id = facebook.marketplace_selector('33461')[0]['id']

    search_term = 'trailer'
    payload = {
        'location_id': location_id,
        'parameters': {
            'minPrice': 100,
            'maxPrice': 2000,
            'daysSinceListed': 1,
            'sortBy': 'creation_time_descend',
            'query': search_term
        },
        'filter': ['rent', 'down payment', 'habitación', 'pintura'],
        'credentials': {
            'user': ,
            'password':
        }
    }
    scrapper = scrapping_selenium.Scrapper({
        'is_headless': True,
        'start_maximized': True,
        'get_details': False,
        'check_scammers': True,
    })
    return scrapper.marketplace_search(payload)


if __name__ == '__main__':
    app.run(debug=True)
