from mine import trend_utils
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import date_utils
import ccxt
import time

df1 = pd.read_csv('/root/trading/trading/data/20200101-binance_futures-1h.csv')
binance = ccxt.binance()
btc = binance.fetch_ticker("BTC/USDT")

a = trend_utils.trend(df1[len(df1)-20:].reset_index(drop=True),20)
print(a.near_trend(btc['close']), a.direction(),a.f_max(time.time()), a.f_min(time.time()))
a.graph(df1)

