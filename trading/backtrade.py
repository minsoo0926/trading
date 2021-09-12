import matplotlib
import matplotlib.pyplot as plt 
from datetime import datetime 
import backtrader as bt
import mine
import pandas as pd
from mine import trend_utils
from pandas_datareader import data
import strategies
import strategy

class MyCSVData(bt.feeds.GenericCSVData):
    params = (
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('datetime', None),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        
    )

df=pd.read_csv('/root/trading/trading/data/20200101-ETH_future.csv')
df['datetime']=pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')
df1=df.set_index('datetime', drop=True)
cerebro = bt.Cerebro()
#data = MyCSVData(dataname='/root/trading/trading/data/20200101-ETH_future.csv', fromdate=datetime(2020, 5, 1))
data=bt.feeds.PandasData(dataname=df1, datetime=None)
cerebro.adddata(data)

cerebro.broker.setcash(500000)
cerebro.broker.setcommission(commission=0.0075, leverage=3.0)
cerebro.addstrategy(strategies.trend_strategy)
cerebro.run()
#Get final portfolio Value 
portvalue = cerebro.broker.getvalue() 
pnl = portvalue - 500000
#Print out the final result 
print('Final Portfolio Value: ${}'.format(portvalue)) 
print('P/L: ${}'.format(pnl)) 
print((portvalue-500000)/500000*100,'%') 
#Visualize 
figure=cerebro.plot(iplot=False)