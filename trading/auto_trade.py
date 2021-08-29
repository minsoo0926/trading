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
import pickle


def table(values):
    first = values[0]
    keys = list(first.keys()) if isinstance(first, dict) else range(0, len(first))
    widths = [max([len(str(v[k])) for v in values]) for k in keys]
    string = ' | '.join(['{:<' + str(w) + '}' for w in widths])
    return "\n".join([string.format(*[str(v[k]) for k in keys]) for v in values])


def date_from_timestamp(timestamp):
    return(timestamp/1000)


config = configparser.ConfigParser()
config.read('/root/trading/config.ini')

API_KEY = config['BINANCE']['API_KEY']
SECRET_KEY = config['BINANCE']['SECRET_KEY']
API_URL = config['BINANCE']['API_URL']

exchange_id = 'binance'
exchange = ccxt.binance({
    'options': {
        'adjustForTimeDifference': True,
        'defaultType': 'future'
    },
    'enableRateLimit': True,
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
})

binance=ccxt.binance({
    'options': {
        'adjustForTimeDifference': True,
        # 'defaultType': 'future'
    },
    'rateLimit': 10000,
    'enableRateLimit': True,
    # 'verbose': True,
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
})

nest_asyncio.apply()

BINANCE_SYMBOL = 'ETH/USDT'


async def hour():
    global trend
    global data
    print('hour')
    f=open('/root/trading/trading/data/log.txt', 'a')
    f.write(time.ctime()+' running...\n')
    f.close()
    since = data['datetime'][len(data)-1]
    since_timestamp = binance.parse8601(since)
    
    data_1h = ccxt_utils.fetch_ohlcv(BINANCE_SYMBOL, binance, timeframe='1h', start=since, end=None)
    data_1h_df = ccxt_utils.ohlcv_to_df(data_1h['data'])
    data_1h_df.to_csv('/root/trading/trading/data/temp.csv')
    
    data_1h_df=pd.read_csv('/root/trading/trading/data/temp.csv').reset_index(drop=True)
    data=data.reset_index(drop=True)
    total=pd.concat([data, data_1h_df[1:]], ignore_index=True)

    d=total[len(data)-80:len(data)].reset_index(drop=True)
    trend=trend_utils.trend(d)
    data=total
    total=total.set_index('datetime',append=False)
    total.to_csv('/root/trading/trading/data/20200101-ETH.csv')
    await asyncio.sleep(3600)
    
    
async def minute():
    print('minute')
    global data
    global trend
    global temp_position
    
    log=[]
    d=data[len(data)-80:len(data)]
    temp_price= binance.fetch_ticker('ETH/USDT')['close']
    position=trend.near_trend(temp_price)
    if position == 'buy' and not temp_position=='buy':
        if market.get_BNBbalance()>=0.03:
            order= binance.create_market_sell_order('BNB/USDT', market.get_BNBbalance())
        
        if market.get_USDTbalance()>=10:
            order = binance.create_market_buy_order('ETH/USDT', market.get_USDTbalance()/binance.fetch_ticker('ETH/USDT')['high'])
        
        log.append([time.ctime(), 'buy', '-'])
        temp_position='buy'
        record=pd.DataFrame(log, columns=['datetime','position','amount'])
        record.to_csv("/root/trading/trading/data/trading.csv", mode="a")
    elif position == 'sell' and not temp_position=='sell':
        
        if market.get_USDTbalance()<10:
            order = binance.create_market_sell_order('ETH/USDT', market.get_ETHbalance())
        
        log.append([time.ctime(), 'sell', market.get_USDTbalance()])
        temp_position='sell'
        record=pd.DataFrame(log, columns=['datetime','position','amount'])
        record.to_csv("/root/trading/trading/data/trading.csv", mode="a")
    
    await asyncio.sleep(60)

async def min_loop():
    while True:
        await minute()
async def hour_loop():
    while True:
        await hour()

async def main():
    global data
    global trend
    global temp_position
    await asyncio.gather(min_loop(), hour_loop())

data=pd.read_csv('/root/trading/trading/data/20200101-ETH.csv').reset_index(drop=True)
trend=trend_utils.trend(data[len(data)-80:len(data)].reset_index(drop=True))
log=pd.read_csv('/root/trading/trading/data/trading.csv', delimiter=',')
temp_position=log['position'][len(log)-1]

loop=asyncio.get_event_loop()
try:
    loop.run_until_complete(main())  
except KeyboardInterrupt:
    print('end')
loop.close()

f=open('/root/trading/trading/data/log.txt', 'a')
f.write(time.ctime()+' end\n')
f.close()
 
