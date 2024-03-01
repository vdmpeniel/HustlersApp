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


def marketplace_selector(term):
    variables = {
        "params": {
            "caller": "MARKETPLACE",
            "country_filter": 'null',
            "integration_strategy": "STRING_MATCH",
            "page_category": ["CITY", "SUBCITY", "NEIGHBORHOOD", "POSTAL_CODE"],
            "query": term,
            "search_type": "PLACE_TYPEAHEAD"
        }
    }
    url_encoded_variables = '&variables=' + quote(json.dumps(obj=variables, indent=4).replace(' ', ''))

    headers = {
        'authority': 'www.facebook.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'sb=jfiZZXcq4bYruIkySrRGoUxP; datr=jfiZZQxdx0fNPQCzrcJooPOj; c_user=100000646540895; ps_n=0; ps_l=0; wd=1438x707; xs=39%3AJrHqs4KmQ6ITPg%3A2%3A1704589623%3A-1%3A4523%3A%3AAcWKoekgs445Wz_G-33Av-2Nlv37sHhDZQHNqMfV4YY; fr=1CjEcvEkjqtMCW12U.AWVlKua8Xu0LN2ry4GgYeRjmRC4.Bl36nc..AAA.0.0.Bl36nc.AWVEH7lcCuw; usida=eyJ2ZXIiOjEsImlkIjoiQXM5bDg4bzFzeTkzdDgiLCJ0aW1lIjoxNzA5MTU5OTI4fQ%3D%3D; presence=C%7B%22lm3%22%3A%22u.100072482562866%22%2C%22t3%22%3A%5B%7B%22o%22%3A0%2C%22i%22%3A%22u.100004902189106%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7084097001708204%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.100043986742939%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.757457289%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.6880455278731946%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.6982910475171440%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.100001651610376%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.5552565714866970%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7295282217229276%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7363243583696293%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.769554540%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.655568087896044%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7340852102650757%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7585588648141133%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7228629927219593%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7455703891134734%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7262736090449958%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.100009878265549%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7432698196816693%22%7D%5D%2C%22utc3%22%3A1709159951299%2C%22v%22%3A1%7D',
        'dpr': '1',
        'origin': 'https://www.facebook.com',
        'referer': 'https://www.facebook.com/marketplace',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121")',
        'sec-ch-ua-full-version-list': '"Not A(Brand";v="99.0.0.0", "Google Chrome";v="121.0.6167.184", "Chromium";v="121.0.6167.184"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '',
        'sec-ch-ua-platform': 'macOS',
        'sec-ch-ua-platform-version': '11.7.10',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'viewport-width': '511',
        'x-asbd-id': '129477',
        'x-fb-friendly-name': 'CometMarketplaceSetBuyLocationMutation',
        'x-fb-lsd': 'Ja6t5k6HchlC_pfZJiNAxt'
    }

    payload = {
        "referrer": "https://www.facebook.com/marketplace/104082902960678/vehicles/?exact=false",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": (
            f"av=100000646540895"
            "&__aaid=0"
            "&__user=100000646540895&__a=1"
            "&__req=7n"
            "&__hs=19781.HYP%3Acomet_pkg.2.1..2.1"
            "&dpr=1"
            "&__ccg=EXCELLENT"
            "&__rev=1011712572"
            "&__s=927f4u%3Acl6hlb%3Atv34gr"
            "&__hsi=7340749290228644467"
            "&__dyn=7AzHK4HwBgDx-5Q1ryaxG4Qih09y2O5U4e2CEf8jyUW3qi7UK360CEboG4E2vwpUe8hw8u250n82nwb-q7oc81xoswMwto88422y11xmfz822wtU7m4oaEnxO0Bo4O2-2l2Utwwg4u0Mo4G1hx-3m1mzXw8W58jwGzEjxq1jxS6FobrwKxm5o6Kexfxmu3W3y2616DBx_xWcwfCm2CVEbUGdG1Fwh85d08O321LyUaUcojxK2B0LwnU8oC1Hg6C13xe3a3G3WfKufxa3m"
            "&__csr=hthsAhfktaytt4hexIh9T4th2RfsLNibbq9iiiYVcBHkUxF5GLn9Z_YXh6RvTXaQWAGhbGKF6AWGGGSlkRUZrih9FlGWleV8ClJ7AySmqblrGAFm-y2RX-GiDj--bybQ4K9WAjCFoHyF69HCgyaggUKngSuKAaF2A58CUhyFrxqGuAZ3pXDzElGWCiKjAzAexady8CUO5VEyUkDyoK2924dUWFFWAx26F98hxXKAbF0-Byo98G2CQ6rCxLouy8CfxefyEGKUWm1hwRxi26mUC68Iwy1HxKq9g-7XhKfgeUWfBAQdxq1vgiwSwslK2e48kwIyUmCzu2yconwwADwGy8gwEwBwRwywzwFx6iaxK8wExudxS5K361mDAx-bxmGUx3UkzpEvUnxa5UOi1ewXzE987e33Kq4U24iw8O2G6E4eWwloy223i1gg8E16k3658owIDg8E6Nwh8Xzqy_gyu2y2S4U4KbCDDGE-Wxa0E8hG2TwsEeE0Ae0g-0eFfDmtO05oK06rk0su04so0g-o4y3h0k80kKK01MDK01gKhEx2FUO1VyU0wC0F8mCwbng23w3Fo0xe0ja0fgw17207mE0Qi18w9O0XW9Uiwfuh55UAAGz2Hx1liiexkk1jKEUjyRjy80Vui0vW0_UB00C_GmOP0krw36o511x0VxlFyo09oU3iwRAqw29Fng0VWlwSgdHx26ojw8uu04Pojxm"
            "&__comet_req=15"
            "&fb_dtsg=NAcPgJm08HJ69clYiPGZHUo7EjVWxk3mDwTj5-zdYzMfLBVLSK925ow%3A39%3A1704589623"
            "&jazoest=25357"
            "&lsd=Ja6t5k6HchlC_pfZJiNAxt"
            "&__spin_r=1011712572"
            "&__spin_b=trunk"
            "&__spin_t=1709151382"
            "&fb_api_caller_class=RelayModern"
            "&fb_api_req_friendly_name=MarketplaceSearchAddressDataSourceQuery"
            f"&variables={url_encoded_variables}"
            "&server_timestamps=true"
            "&doc_id=7321914954515895"
        ),
        "credentials": "include"
    }

    response = requests.request(
        method='POST',
        url='https://www.facebook.com/api/graphql/',
        json=payload,
        headers=headers
    )

    content = json.loads(response.content)
    if 'data' not in content:
        return {}
    edges = content['data']['city_street_search']['street_results']['edges']

    location_list = []
    for node in edges:
        # print('TYPE: ' + str(type(node)))
        if type(node) is dict:
            location_list.append({
                'id': node['node']['page']['id'],
                'address': node['node']['single_line_address'],
                'location': node['node']['location']
            })
    return location_list


if __name__ == '__main__':
    location_id = marketplace_selector('33461')[0]['id']
    # scrapping_splinter.marketplace_search('trailer', location_id)

    search_term = 'trailer'
    payload = {
        'location_id': location_id,
        'parameters': {
            'minPrice': 100,
            'maxPrice': 2000,
            'daysSinceListed': 1,
            'sortBy': 'creation_time_descend',
            'query': search_term
        }
    }
    scrapper = scrapping_selenium.Scrapper({
        'is_headless': True,
        'start_maximized': True,
        'get_details': False,
        'check_scammers': True
    })
    scrapper.marketplace_search(payload)
