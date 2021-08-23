import matplotlib
import matplotlib.pyplot as plt 
from datetime import datetime 
import backtrader as bt
import mine
import pandas as pd
from mine import trend_utils
from pandas_datareader import data
import strategies


cerebro = bt.Cerebro()
data = bt.feeds.YahooFinanceData(dataname='data/BTC-USD.csv', fromdate=datetime(2020, 1, 1), todate=datetime(2021, 8, 21))
cerebro.adddata(data)

cerebro.broker.setcash(10000000)
cerebro.broker.setcommission(commission=0.0075)
cerebro.addstrategy(strategies.trend_strategy)
cerebro.run()
#Get final portfolio Value 
portvalue = cerebro.broker.getvalue() 
pnl = portvalue - 10000000 
#Print out the final result 
print('Final Portfolio Value: ${}'.format(portvalue)) 
print('P/L: ${}'.format(pnl)) 
print((portvalue-10000000)/10000000*100,'%') 
#Visualize 
cerebro.plot()
