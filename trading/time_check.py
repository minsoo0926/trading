from binance.client import Client
import binance
import configparser
import json
import requests
import ccxt
from pprint import pprint 
from mine import market, trend_utils
import asyncio
import nest_asyncio
import time
from datetime import datetime, timezone
import pandas as pd
from utils import ccxt_utils

config = configparser.ConfigParser()
config.read('/root/trading/config.ini')

API_KEY = config['BINANCE']['API_KEY']
SECRET_KEY = config['BINANCE']['SECRET_KEY']
API_URL = config['BINANCE']['API_URL']

client = Client(API_KEY, SECRET_KEY)

while True:
    local_time1 = int(time.time() * 1000)
    server_time = client.get_server_time()
    diff1 = server_time['serverTime'] - local_time1
    local_time2 = int(time.time() * 1000)
    diff2 = local_time2 - server_time['serverTime']
    print("local1: %s server:%s local2: %s diff1:%s diff2:%s" % (local_time1, server_time['serverTime'], local_time2, diff1, diff2))
    time.sleep(2)
