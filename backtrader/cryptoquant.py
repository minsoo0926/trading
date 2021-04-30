
import pandas as pd 
import os, sys
from datetime import datetime

import requests
from pprint import pprint 
import configparser
from urllib.parse import urljoin 
from pprint import pprint 
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read('../config.ini')

API_KEY = config['CRYPTOQUANT']['API_KEY']
API_URL = config['CRYPTOQUANT']['API_URL']
LIMIT = 100000 
CQ_DATE_FORMAT = '%Y%m%dT%H%M%S'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


headers = {'Authorization': 'Bearer ' + API_KEY}


def str_to_datetime(date_str, format):
    return(datetime.strptime(date_str, format))


def datetime_to_str(datetime_obj, format):
    return(datetime.strftime(datetime_obj, format))


# start, end: datetime_str 
def coinbase_premium_big_df(start=None, end=None, tick='min'):

    data = []

    PATH = 'btc/market-data/coinbase-premium-index'
    URL = urljoin(API_URL, PATH)

    start_time = str_to_datetime(start, CQ_DATE_FORMAT)
    end_time = str_to_datetime(end, CQ_DATE_FORMAT)
    # num_mins = (end_time - start_time).days *24 * 60

    while start_time < end_time:
        
        params = {
            'window': 'min',
            'from': start,
            'to': end, 
            'limit': 100000,
        }

        response = requests.get(URL, headers=headers, params=params).json()
        coinbase_premium_index = response['result']['data']
        
        data += coinbase_premium_index

        end_time = str_to_datetime(coinbase_premium_index[-1]['datetime'], DATE_FORMAT) - timedelta(minutes=1)
        end = datetime.strftime(end_time, CQ_DATE_FORMAT)

    
    coinbase = pd.DataFrame(data).set_index('datetime')
    return(coinbase.iloc[::-1])


def price_big_df(start=None, end=None, tick='min'):

    data = []

    PATH = 'btc/market-data/price-usd'
    URL = urljoin(API_URL, PATH)

    start_time = str_to_datetime(start, CQ_DATE_FORMAT)
    end_time = str_to_datetime(end, CQ_DATE_FORMAT)

    while start_time < end_time:

        params = {
            'window': 'min',
            'from': start,
            'to': end, 
            'limit': 100000,
        }

        response = requests.get(URL, headers=headers, params=params).json()
        price = response['result']['data']
        
        data += price

        end_time = str_to_datetime(price[-1]['datetime'], DATE_FORMAT) - timedelta(minutes=1)
        end = datetime.strftime(end_time, CQ_DATE_FORMAT)

    
    coinbase = pd.DataFrame(data).set_index('datetime')
    return(coinbase.iloc[::-1])


# tick: min 
def coinbase_premium_df(start=None, end=None, tick='min', limit=100):

    PATH = 'btc/market-data/coinbase-premium-index'
    URL = urljoin(API_URL, PATH)
    params = {
        'window': tick,
        'from': start,
        'to': end, 
        'limit': limit,
    }

    response = requests.get(URL, headers=headers, params=params).json()
    coinbase_premium_index = response['result']['data']
    coinbase = pd.DataFrame(coinbase_premium_index).set_index('datetime')

    return(coinbase.iloc[::-1])

# tick: min, block, hour, day 
def price_df(to, tick='min', limit=100):
    
    PATH = 'btc/market-data/price-usd'
    URL = urljoin(API_URL, PATH)
    params = {
        'window': tick,
        'to': to,
        'limit': limit 
    }

    response = requests.get(URL, headers=headers, params=params).json()
    price_usd = response['result']['data']
    price = pd.DataFrame(price_usd).set_index('datetime')
    return(price.iloc[::-1])

