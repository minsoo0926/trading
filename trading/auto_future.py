#futures
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

config = configparser.ConfigParser()
config.read('/root/trading/config.ini')

API_KEY = config['BINANCE_FUTURE']['API_KEY']
SECRET_KEY = config['BINANCE_FUTURE']['SECRET_KEY']
API_URL = config['BINANCE_FUTURE']['API_URL']

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
        'defaultType': 'future'
    },
    'rateLimit': 10000,
    'enableRateLimit': True,
    # 'verbose': True,
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
})

markets = binance.load_markets()
symbol = "BTC/USDT"
m = binance.market(symbol)
leverage = 20
size = 20

resp = binance.fapiPrivate_post_leverage({
    'symbol': m['id'],
    'leverage': leverage
})

nest_asyncio.apply()

BINANCE_SYMBOL = 'BTC/USDT'


async def hour():
    global trend
    global data
    f=open('/root/trading/trading/data/log_future.txt', 'a')
    f.write(time.ctime()+' running...\n')
    f.close()
    since = data['datetime'][len(data)-2]
    since_timestamp = binance.parse8601(since)
    
    data_1h = ccxt_utils.fetch_ohlcv(BINANCE_SYMBOL, binance, timeframe='1h', start=since, end=None)
    data_1h_df = ccxt_utils.ohlcv_to_df(data_1h['data'])
    data_1h_df.to_csv('/root/trading/trading/data/temp_future.csv')
    
    data_1h_df=pd.read_csv('/root/trading/trading/data/temp_future.csv').reset_index(drop=True)
    data=data.reset_index(drop=True)
    total=pd.concat([data[:-2], data_1h_df], ignore_index=True)

    d=total[len(data)-size:len(data)].reset_index(drop=True)
    trend=trend_utils.trend(d, size)
    data=total
    total=total.set_index('datetime',append=False)
    total.to_csv('/root/trading/trading/data/20200101-binance_futures-1h.csv')
    await asyncio.sleep(300)
    
    
async def minute():
    global data
    global trend
    global temp_position
    
    log=[]
    d=data[len(data)-20:len(data)]
    try:
        temp_price= binance.fetch_ticker('BTC/USDT')['close']
    except:
        print(time.ctime()+'error!!!')
        f=open('/root/trading/trading/data/log_future.txt', 'a')
        f.write(time.ctime()+' error!!!\n')
        f.close()
        return

    position=trend.near_trend(temp_price)

    if position=='buy' and temp_position=='none':
        try:
            order = binance.create_market_buy_order('BTC/USDT', leverage*market.get_USDTbalance_future()/binance.fetch_ticker('BTC/USDT')['high'])
            log.append([time.ctime(), 'buy', '-'])
            temp_position='buy'
            record=pd.DataFrame(log, columns=['datetime','position','amount'])
            record.to_csv("/root/trading/trading/data/trading_future.csv", mode="a")    
        except:
            print('insufficient margin')
    elif position == 'sell' and temp_position=='none':
        try:
            order = binance.create_market_sell_order('BTC/USDT', leverage*market.get_USDTbalance_future()/binance.fetch_ticker('BTC/USDT')['high'])
            log.append([time.ctime(), 'sell', '-'])
            temp_position='sell'
            record=pd.DataFrame(log, columns=['datetime','position','amount'])
            record.to_csv("/root/trading/trading/data/trading_future.csv", mode="a")
        except:
            print('insufficient margin')
    elif position == 'buy' and temp_position=='sell':
        try:
            order = binance.create_market_buy_order('BTC/USDT', 2*market.get_BTCbalance_future(leverage))   
            log.append([time.ctime(), 'buy', '-'])
            temp_position='buy'
            record=pd.DataFrame(log, columns=['datetime','position','amount'])
            record.to_csv("/root/trading/trading/data/trading_future.csv", mode="a")
        except:
            print('insufficient margin')
    elif position == 'sell' and temp_position=='buy':
        try:    
            order = binance.create_market_sell_order('BTC/USDT', 2*market.get_BTCbalance_future(leverage)) 
            log.append([time.ctime(), 'sell', '-'])
            temp_position='sell'
            record=pd.DataFrame(log, columns=['datetime','position','amount'])
            record.to_csv("/root/trading/trading/data/trading_future.csv", mode="a")
        except:
            print('insufficient margin')
    elif position == 'none' and temp_position=='sell':
        try:
            order = binance.create_market_buy_order('BTC/USDT', market.get_BTCbalance_future(leverage))
            
            log.append([time.ctime(), 'none', market.get_USDTbalance_future()])
            temp_position='none'
            record=pd.DataFrame(log, columns=['datetime','position','amount'])
            record.to_csv("/root/trading/trading/data/trading_future.csv", mode="a")
        except:
            print('insufficient margin')
    elif position == 'none' and temp_position=='buy':
        try:
            order = binance.create_market_sell_order('BTC/USDT', market.get_BTCbalance_future(leverage))
            
            log.append([time.ctime(), 'none', market.get_USDTbalance_future()])
            temp_position='none'
            record=pd.DataFrame(log, columns=['datetime','position','amount'])
            record.to_csv("/root/trading/trading/data/trading_future.csv", mode="a")
        except:
            print('insufficient margin')
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
    
data=pd.read_csv('/root/trading/trading/data/20200101-binance_futures-1h.csv').reset_index(drop=True)
trend=trend_utils.trend(data[len(data)-size:len(data)].reset_index(drop=True), size)
log=pd.read_csv('/root/trading/trading/data/trading_future.csv', delimiter=',')
temp_position=log['position'][len(log)-1]

loop=asyncio.get_event_loop()
while True:
    try:
        loop.run_until_complete(main())  
    except KeyboardInterrupt:
        print('end')
        loop.close()
        break
    else:
        print('error!')
        loop.close()
        continue

f=open('/root/trading/trading/data/log_future.txt', 'a')
f.write(time.ctime()+' end\n')
f.close()
