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
        'apiKey' : '',
        'secret' : '',
    })
    balance=binance.fetch_balance()
    return (balance['BNB']['free'])
    
def get_BTCbalance():
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : '',
        'secret' : '',
    })
    balance=binance.fetch_balance()
    return (balance['BTC']['free'])
    
    
def get_USDTbalance():
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : '',
        'secret' : '',
    })
    balance=binance.fetch_balance()
    return (balance['USDT']['free'])

def get_ETHbalance():
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : '',
        'secret' : '',
    })
    balance=binance.fetch_balance()
    return (balance['ETH']['free'])

    
def get_USDTbalance_future():
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : '',
        'secret' : '',
        'options' : {
            'defaultType': 'future',
            'adjustForTimeDifference': True
        }
    })
    balance=binance.fetch_balance()
    return (balance['USDT']['free'])

def get_ETHbalance_future(leverage):
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : '',
        'secret' : '
        'options' : {
            'defaultType': 'future',
            'adjustForTimeDifference': True
        }
    })
    balance=binance.fetch_balance()
    amount=leverage*balance['USDT']['used']/binance.fetch_ticker('ETH/USDT')['close']
    return amount

def get_BTCbalance_future(leverage):
    #잔고보기
    binance=ccxt.binance({
        'apiKey' : '',
        'secret' : '',
        'options' : {
            'defaultType': 'future',
            'adjustForTimeDifference': True
        }
    })
    balance=binance.fetch_balance()
    amount=leverage*balance['USDT']['used']/binance.fetch_ticker('BTC/USDT')['close']
    return amount
