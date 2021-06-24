
import pandas as pd 
import os, sys
from datetime import datetime

import requests
from pprint import pprint 
import configparser
from urllib.parse import urljoin 
from pprint import pprint 
from datetime import datetime, timedelta
from utils import merge_price_signal, time_format_conversion

config = configparser.ConfigParser()
config.read('../config.ini')

API_KEY = config['CRYPTOQUANT']['API_KEY']
API_URL = config['CRYPTOQUANT']['API_URL']

LIMIT = 100000 

CQ_DATE_FORMAT = '%Y%m%dT%H%M%S'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


headers = {'Authorization': 'Bearer ' + API_KEY}


def str_to_datetime(date_str, format):
    '''
    change str date to datetime using format parameter  
    '''
    return(datetime.strptime(date_str, format))


def datetime_to_str(datetime_obj, format):
    '''
    change datetime  to str date using format parameter  
    '''
    return(datetime.strftime(datetime_obj, format))


# start, end: datetime_str
# tick: min, hour, day, block  
# 
def coinbase_premium_big_df(start=None, end=None, tick='min'):
    '''
    get data from cryptoquant from start date to end date
    start: date start ('20200301T010000')
    end: date end ('20210430T010000')
    return: data as dataframe format 
    '''
    data = []

    PATH = 'btc/market-data/coinbase-premium-index'
    URL = urljoin(API_URL, PATH)

    start_time = str_to_datetime(start, CQ_DATE_FORMAT)
    end_time = str_to_datetime(end, CQ_DATE_FORMAT)
    # num_mins = (end_time - start_time).days *24 * 60

    while start_time < end_time:
        
        params = {
            'window': tick,
            'from': start,
            'to': end, 
            'limit': LIMIT,
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
            'window': tick,
            'from': start,
            'to': end, 
            'limit': LIMIT,
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


def get_price_coinbase_premium_df(limit=100, tick='min'):
    coinbase = coinbase_premium_df(limit=limit)
    new_date = time_format_conversion(coinbase.index[-1])
    print(new_date)
    price = price_df(to=new_date, limit=limit)

    price.index = pd.to_datetime(price.index)
    coinbase.index = pd.to_datetime(coinbase.index)

    return(merge_price_signal(price, coinbase))


def get_price_coinbase_premium_big_df(start=None, end=None, tick='min'):
    '''
    get price & coinbase premium data from cryptoquant from start date to end date
    start: date start ('20200301T010000')
    end: date end ('20210430T010000')
    return: data as dataframe format 
    '''

    # get the data (start - end) from cryptoquant
    coinbase_df = coinbase_premium_big_df(start, end, tick)
    price_df = price_big_df(start, end, tick)

    # set the index as datetime format 
    price_df.index = pd.to_datetime(price_df.index)
    coinbase_df.index = pd.to_datetime(coinbase_df.index)

    # merge two data using index as a key and return 
    return(merge_price_signal(price_df, coinbase_df))