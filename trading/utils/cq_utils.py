
# import pandas as pd
import os
import sys
from datetime import datetime, timedelta
import requests
import configparser
from urllib.parse import urljoin

from .date_utils import validate_dateformat, str_to_datetime
# from utils import merge_price_signal, time_format_conversion


config = configparser.ConfigParser()
config.read('../config.ini')

API_KEY = config['CRYPTOQUANT']['API_KEY']
API_URL = config['CRYPTOQUANT']['API_URL']

DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
CQ_DATE_FORMAT = '%Y%m%dT%H%M%S'
CQ_RETURNED_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
CQ_RETURNED_DATE_FORMAT_DATE_ONLY = '%Y-%m-%d'

LIMIT = 100000

HEADERS = {'Authorization': 'Bearer ' + API_KEY}


def copro_premium(start, end=None, timeframe='min'):
    '''
    get data from cryptoquant from start date to end date
    start: date start ('2020-03-01 01:00:00') - data available starting from '2020-01-01
    end: date end ('2021-04-30 01:00:00')
    return: data
    for return data format check cryptoquant site 
    }
    '''

    if (not validate_dateformat(start)):
        return {'status': 'error', 'message': 'param start is not a correct date format.'}
        # return('start is not a correct date format. ')

    if (end != None) and (not validate_dateformat(end)):
        return {'status': 'error', 'message': 'param end is not a correct date format.'}
        # return('end is not a correct date format. ')

    start_time = str_to_datetime(start)
    if (end != None):
        end_time = str_to_datetime(end)
    else:
        end_time = datetime.utcnow()


    data = []

    PATH = 'btc/market-data/coinbase-premium-index'
    URL = urljoin(API_URL, PATH)

    while start_time < end_time:
        print(f'processing: {start_time} - {end_time}')

        params = {
            'window': timeframe,
            'from': start_time.strftime(CQ_DATE_FORMAT),
            'to': end_time.strftime(CQ_DATE_FORMAT),
            'limit': LIMIT,
        }

        response = requests.get(URL, headers=HEADERS, params=params).json()
        # print(response)
        
        if response['status']['code'] != 200: 
            return {'status': 'error', 'message': 'something wrong in response'}

        coinbase_premium_index = response['result']['data']

        if (len(coinbase_premium_index) != 0): 
            data += coinbase_premium_index
            end_time = str_to_datetime(coinbase_premium_index[-1]['datetime'], CQ_RETURNED_DATE_FORMAT) - timedelta(minutes=1)
        else:
            end_time = start_time 

    return({'status': 200, 'data': data[::-1]})


def stablecoin_supply_ratio(start, end=None, timeframe='day'):
    '''
    returns SSR(Stablecoin Supply Ratio) - a ratio of stablecoin supply in the whole cryptocurrency market
    where stablecoin is used as fiat substitute for trading.
    This means that the supply of stablecoin can be used to assess the potential buying pressure for bitcoin.
    The historical starting point is 2017-11-28 00:00:00.
    '''
    if (not validate_dateformat(start)):
        return {'status': 'error', 'message': 'param start is not a correct date format.'}
        # return('start is not a correct date format. ')

    if (end != None) and (not validate_dateformat(end)):
        return {'status': 'error', 'message': 'param end is not a correct date format.'}
        # return('end is not a correct date format. ')

    start_time = str_to_datetime(start)
    if (end != None):
        end_time = str_to_datetime(end)
    else:
        end_time = datetime.utcnow()


    data = []

    PATH = 'btc/market-indicator/stablecoin-supply-ratio'
    URL = urljoin(API_URL, PATH)

    while start_time < end_time:
        print(f'processing: {start_time} - {end_time}')

        params = {
            'window': timeframe, 
            'from': start_time.strftime(CQ_DATE_FORMAT),
            'to': end_time.strftime(CQ_DATE_FORMAT),
            'limit': LIMIT,
        }

        response = requests.get(URL, headers=HEADERS, params=params).json()
        # print(response)

        if response['status']['code'] != 200: 
            return {'status': 'error', 'message': 'something wrong in response'}

        # print(response['result']['data'])
        ssr = response['result']['data']

        if (len(ssr) != 0): 
            data += ssr
            end_time = str_to_datetime(ssr[-1]['date'], CQ_RETURNED_DATE_FORMAT_DATE_ONLY) - timedelta(days=1)
        else:
            end_time = start_time 

    return({'status': 200, 'data': data[::-1]})


def exchange_btc_reserve(start, end=None, exchange='all_exchange', timeframe='block'):
    '''
    get data from cryptoquant from start date to end date
    start: date start ('2020-03-01 01:00:00')
    end: date end ('2021-04-30 01:00:00')
    return: data
    '''

    if (not validate_dateformat(start)):
        return {'status': 'error', 'message': 'param start is not a correct date format.'}
        # return('start is not a correct date format. ')

    if (end != None) and (not validate_dateformat(end)):
        return {'status': 'error', 'message': 'param end is not a correct date format.'}
        # return('end is not a correct date format. ')

    start_time = str_to_datetime(start)
    if (end != None):
        end_time = str_to_datetime(end)
    else:
        end_time = datetime.utcnow()


    data = []

    PATH = 'btc/exchange-flows/reserve'
    URL = urljoin(API_URL, PATH)

    while start_time < end_time:
        print(f'processing: {start_time} - {end_time}')

        params = {
            'exchange': exchange, 
            'window': timeframe,
            'from': start_time.strftime(CQ_DATE_FORMAT),
            'to': end_time.strftime(CQ_DATE_FORMAT),
            'limit': LIMIT,
        }

        response = requests.get(URL, headers=HEADERS, params=params).json()
        # print(response)

        if response['status']['code'] != 200: 
            return {'status': 'error', 'message': 'something wrong in response'}

        # print(response['result']['data'])
        reserve = response['result']['data']

        if (len(reserve) != 0): 
            data += reserve
            end_time = str_to_datetime(reserve[-1]['datetime'], CQ_RETURNED_DATE_FORMAT) - timedelta(minutes=1)
        else:
            end_time = start_time 

    return({'status': 200, 'data': data[::-1]})


def exchange_btc_inflow(start, end=None, exchange='all_exchange', timeframe='block'):
    '''
    get data from cryptoquant from start date to end date
    start: date start ('2020-03-01 01:00:00')
    end: date end ('2021-04-30 01:00:00')
    return: data
    '''

    if (not validate_dateformat(start)):
        return {'status': 'error', 'message': 'param start is not a correct date format.'}
        # return('start is not a correct date format. ')

    if (end != None) and (not validate_dateformat(end)):
        return {'status': 'error', 'message': 'param end is not a correct date format.'}
        # return('end is not a correct date format. ')

    start_time = str_to_datetime(start)
    if (end != None):
        end_time = str_to_datetime(end)
    else:
        end_time = datetime.utcnow()


    data = []

    PATH = 'btc/exchange-flows/inflow' 
    URL = urljoin(API_URL, PATH)

    while start_time < end_time:
        print(f'processing: {start_time} - {end_time}')

        params = {
            'exchange': exchange, 
            'window': timeframe,
            'from': start_time.strftime(CQ_DATE_FORMAT),
            'to': end_time.strftime(CQ_DATE_FORMAT),
            'limit': LIMIT,
        }

        response = requests.get(URL, headers=HEADERS, params=params).json()
        # print(response)

        if response['status']['code'] != 200: 
            return {'status': 'error', 'message': 'something wrong in response'}

        # print(response['result']['data'])
        inflow = response['result']['data']

        if (len(inflow) != 0): 
            data += inflow
            end_time = str_to_datetime(inflow[-1]['datetime'], CQ_RETURNED_DATE_FORMAT) - timedelta(minutes=1)
        else:
            end_time = start_time 

    return({'status': 200, 'data': data[::-1]})


def exchange_btc_netflow(start, end=None, exchange='all_exchange', timeframe='block'):
    '''
    get data from cryptoquant from start date to end date
    start: date start ('2020-03-01 01:00:00')
    end: date end ('2021-04-30 01:00:00')
    return: data
    '''

    if (not validate_dateformat(start)):
        return {'status': 'error', 'message': 'param start is not a correct date format.'}
        # return('start is not a correct date format. ')

    if (end != None) and (not validate_dateformat(end)):
        return {'status': 'error', 'message': 'param end is not a correct date format.'}
        # return('end is not a correct date format. ')

    start_time = str_to_datetime(start)
    if (end != None):
        end_time = str_to_datetime(end)
    else:
        end_time = datetime.utcnow()

    print(start_time, end_time)

    data = []

    PATH = 'btc/exchange-flows/netflow' 
    URL = urljoin(API_URL, PATH)

    while start_time < end_time:
        print(f'processing: {start_time} - {end_time}')

        params = {
            'exchange': exchange, 
            'window': timeframe,
            'from': start_time.strftime(CQ_DATE_FORMAT),
            'to': end_time.strftime(CQ_DATE_FORMAT),
            'limit': LIMIT,
        }

        response = requests.get(URL, headers=HEADERS, params=params).json()
        # print(response)

        if response['status']['code'] != 200: 
            return {'status': 'error', 'message': 'something wrong in response'}

        # print(response['result']['data'])
        netflow = response['result']['data']

        if (len(netflow) != 0): 
            data += netflow
            end_time = str_to_datetime(netflow[-1]['datetime'], CQ_RETURNED_DATE_FORMAT) - timedelta(minutes=1)
        else:
            end_time = start_time 

    return({'status': 200, 'data': data[::-1]})


def exchange_btc_outflow(start, end=None, exchange='all_exchange', timeframe='block'):
    '''
    get data from cryptoquant from start date to end date
    start: date start ('2020-03-01 01:00:00')
    end: date end ('2021-04-30 01:00:00')
    return: data
    '''

    if (not validate_dateformat(start)):
        return {'status': 'error', 'message': 'param start is not a correct date format.'}
        # return('start is not a correct date format. ')

    if (end != None) and (not validate_dateformat(end)):
        return {'status': 'error', 'message': 'param end is not a correct date format.'}
        # return('end is not a correct date format. ')

    start_time = str_to_datetime(start)
    if (end != None):
        end_time = str_to_datetime(end)
    else:
        end_time = datetime.utcnow()

    print(start_time, end_time)

    data = []

    PATH = 'btc/exchange-flows/outflow' 
    URL = urljoin(API_URL, PATH)

    while start_time < end_time:
        print(f'processing: {start_time} - {end_time}')

        params = {
            'exchange': exchange, 
            'window': timeframe,
            'from': start_time.strftime(CQ_DATE_FORMAT),
            'to': end_time.strftime(CQ_DATE_FORMAT),
            'limit': LIMIT,
        }

        response = requests.get(URL, headers=HEADERS, params=params).json()
        # print(response)

        if response['status']['code'] != 200: 
            return {'status': 'error', 'message': 'something wrong in response'}

        # print(response['result']['data'])
        outflow = response['result']['data']

        if (len(outflow) != 0): 
            data += outflow
            end_time = str_to_datetime(outflow[-1]['datetime'], CQ_RETURNED_DATE_FORMAT) - timedelta(minutes=1)
        else:
            end_time = start_time 

    return({'status': 200, 'data': data[::-1]})


def miners_position_index(start, end=None, timeframe='day'):
    '''
    get data from cryptoquant from start date to end date
    start: date start ('2020-03-01 01:00:00')
    end: date end ('2021-04-30 01:00:00')
    return: data
    '''

    if (not validate_dateformat(start)):
        return {'status': 'error', 'message': 'param start is not a correct date format.'}
        # return('start is not a correct date format. ')

    if (end != None) and (not validate_dateformat(end)):
        return {'status': 'error', 'message': 'param end is not a correct date format.'}
        # return('end is not a correct date format. ')

    start_time = str_to_datetime(start)
    if (end != None):
        end_time = str_to_datetime(end)
    else:
        end_time = datetime.utcnow()

    print(start_time, end_time)

    data = []

    PATH = 'btc/flow-indicator/mpi' 
    URL = urljoin(API_URL, PATH)

    while start_time < end_time:
        print(f'processing: {start_time} - {end_time}')

        params = {
            'window': timeframe,
            'from': start_time.strftime(CQ_DATE_FORMAT),
            'to': end_time.strftime(CQ_DATE_FORMAT),
            'limit': LIMIT,
        }

        response = requests.get(URL, headers=HEADERS, params=params).json()
        # print(response)

        if response['status']['code'] != 200: 
            return {'status': 'error', 'message': 'something wrong in response'}

        # print(response['result']['data'])
        mpi = response['result']['data']

        if (len(mpi) != 0): 
            data += mpi
            end_time = str_to_datetime(mpi[-1]['date'], CQ_RETURNED_DATE_FORMAT_DATE_ONLY) - timedelta(days=1)
        else:
            end_time = start_time 

    return({'status': 200, 'data': data[::-1]})