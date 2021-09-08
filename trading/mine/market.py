from binance.client import Client
import binance
from datetime import datetime 
import configparser
import json
import requests
import ccxt
import time
from pprint import pprint 

def get_BNBbalance():
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : 'iGZ7SwwhHZ02IGg3pYTJGR7dTYHu6T8kIiCVnsDYRreUDTjg6fkTocFi4uHmcv0R',
        'secret' : 'iZot0U2sE7vpZ8AyIp4sBsJrwqib3SVmmSntu4JDnPlEflPXov3qCofcpOQuKwxW',
    })
    balance=binance.fetch_balance()
    return (balance['BNB']['free'])
    
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

def get_ETHbalance():
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : 'iGZ7SwwhHZ02IGg3pYTJGR7dTYHu6T8kIiCVnsDYRreUDTjg6fkTocFi4uHmcv0R',
        'secret' : 'iZot0U2sE7vpZ8AyIp4sBsJrwqib3SVmmSntu4JDnPlEflPXov3qCofcpOQuKwxW',
    })
    balance=binance.fetch_balance()
    return (balance['ETH']['free'])

def get_BTCbalance_future():
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : 'BpLnIGqKodX0EXAxuR14cpbYax4T6Z1KvrQ8Xbevk3PdmcMjO3J06UK9g6IDS1eG',
        'secret' : '90uKFUV4b0HBjOLtmQmSsHdv9rrYGcZlufEwfrnryAfHzT2BB3Xck5ufsfQXnfW9',
        'options' : {
            'defaultType': 'future',
            'adjustForTimeDifference': True
        }
    })
    balance=binance.fetch_balance()
    try: 
        amount=balance['BTC']['free']
    except KeyError:
        amount=0
    return amount
    
    
def get_USDTbalance_future():
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : 'BpLnIGqKodX0EXAxuR14cpbYax4T6Z1KvrQ8Xbevk3PdmcMjO3J06UK9g6IDS1eG',
        'secret' : '90uKFUV4b0HBjOLtmQmSsHdv9rrYGcZlufEwfrnryAfHzT2BB3Xck5ufsfQXnfW9',
        'options' : {
            'defaultType': 'future',
            'adjustForTimeDifference': True
        }
    })
    balance=binance.fetch_balance()
    return (balance['USDT']['free'])

def get_ETHbalance_future():
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : 'BpLnIGqKodX0EXAxuR14cpbYax4T6Z1KvrQ8Xbevk3PdmcMjO3J06UK9g6IDS1eG',
        'secret' : '90uKFUV4b0HBjOLtmQmSsHdv9rrYGcZlufEwfrnryAfHzT2BB3Xck5ufsfQXnfW9',
        'options' : {
            'defaultType': 'future',
            'adjustForTimeDifference': True
        }
    })
    balance=binance.fetch_balance()
    amount=3*balance['USDT']['used']/binance.fetch_ticker('ETH/USDT')['close']
    return amount