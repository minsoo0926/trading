from binance.client import Client
import binance
from datetime import datetime 
import configparser
import json
import requests
import ccxt
import time
from pprint import pprint 

def get_BTCbalance():
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : 'iGZ7SwwhHZ02IGg3pYTJGR7dTYHu6T8kIiCVnsDYRreUDTjg6fkTocFi4uHmcv0R',
        'secret' : 'iZot0U2sE7vpZ8AyIp4sBsJrwqib3SVmmSntu4JDnPlEflPXov3qCofcpOQuKwxW',
    })
    balance=binance.fetch_balance()
    return (balance['BTC']['free'])
    
    
def get_USDTbalance():
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : 'iGZ7SwwhHZ02IGg3pYTJGR7dTYHu6T8kIiCVnsDYRreUDTjg6fkTocFi4uHmcv0R',
        'secret' : 'iZot0U2sE7vpZ8AyIp4sBsJrwqib3SVmmSntu4JDnPlEflPXov3qCofcpOQuKwxW',
    })
    balance=binance.fetch_balance()
    return (balance['USDT']['free'])
