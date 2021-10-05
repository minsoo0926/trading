from mine import  market
import backtrader as bt
import pandas as pd
from utils import date_utils
import numpy as np
import matplotlib.pyplot as plt
import time

class trend:
    def __init__(self, data):
        end = 20
        start= 0
        data=data.reset_index(drop=True)
        max=local_max(data, start, end)
        min=local_min(data, start, end)
        
        z_max=np.polyfit(max['datetime'], max['high'],1)
        self.f_max=np.poly1d(z_max)
        z_min=np.polyfit(min['datetime'], min['low'],1)
        self.f_min=np.poly1d(z_min)

    def direction(self):
        #rising
        if self.f_max[1]>0 and self.f_min[1]>0:
            return 'up'
        #descending
        elif self.f_max[1]<0 and self.f_min[1]<0:
            return 'down'
        else:
            return 'none'

    def near_trend(self, temp_price, datetime):
        if 0.97*self.f_min(datetime)<temp_price<self.f_min(datetime)*(1.01) and self.direction()=='up':
            return 'buy'
        elif 1.03*self.f_max(datetime)>temp_price>self.f_max(datetime)*(0.99) and self.direction()=='down':
            return 'sell'
        else : 
            return 'none' 

    def graph(self, data):
        end=len(data)-1
        start=end-100 
        max=local_max(data, start, end)
        min=local_min(data, start, end)
        d=[]
        for x, y in zip(data['datetime'][0:100], data['close'][0:100]):
            d.append([date_utils.str_to_utctimestamp(x), y])
        df=pd.DataFrame(data=d, columns=['datetime', 'close'])
        #d=data[int(data.index(data['datetime']==max['datetime'][0])):int(data.index(data['datetime']==max['datetime'][len(max)-1]))]
        #plt.plot(df['datetime'], df['close'], 'k')

        plt.plot(max['datetime'], max['high'], 'r')
        plt.plot(min['datetime'], min['low'], 'y')
        y_max=[]
        for x in max['datetime']:
            y_max.append(self.f_max(x))
        plt.plot(max['datetime'], y_max, 'g')
        
        y_min=[]
        for x in max['datetime']:
            y_min.append(self.f_min(x))
        plt.plot(max['datetime'], y_min, 'b')


def local_max(data, start, end):
    max_pts=[[data.datetime[start],data.high[start]]]
    for i in range(start, end-4):
        if data['high'][i]<data['high'][i+2] and data['high'][i+1]<data['high'][i+2] and data['high'][i+3]<data['high'][i+2] and data['high'][i+4]<data['high'][i+2]:
            max_pts.append([data.datetime[i+2],data.high[i+2]])
    max_pts.append([data.datetime[end-1],data.high[end-1]])
    columns=['datetime', 'high']
    df=pd.DataFrame(data=max_pts, columns=columns)
    return df

def local_min(data, start, end):
    min_pts=[[data.datetime[start],data.low[start]]]
    for i in range(start, end-4):
        if data['low'][i]>data['low'][i+2] and data['low'][i+1]>data['low'][i+2] and data['low'][i+3]>data['low'][i+2] and data['low'][i+4]>data['low'][i+2]:
            min_pts.append([data.datetime[i+2],data.low[i+2]])
    min_pts.append([data.datetime[end-1],data.low[end-1]])
    columns=['datetime', 'low']
    df=pd.DataFrame(data=min_pts, columns=columns)
    return df

class trend_strategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        '''
    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size
            elif order.issell():  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

                gross_pnl = (order.executed.price - self.buyprice) * \
                    self.opsize

                gross_pnl *= 5

                net_pnl = gross_pnl - self.buycomm - order.executed.comm
                self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                         (gross_pnl, net_pnl))
'''
    def __init__(self):
        datas=[]
        columns=['datetime', 'high', 'low']
        self.date=self.data.datetime
        self.high=self.data.high
        self.low=self.data.low
        self._close = self.data.close
        for i in range(-20, 0):
            datas.append([self.date[i], self.high[i], self.low[i]])
        datas=pd.DataFrame(columns=columns, data=datas)        
        self.trend=trend(datas)
        
    def next(self):
        datas=[]
        columns=['datetime', 'high', 'low']
        for i in range(-20, 0):
            datas.append([self.date[i], self.high[i], self.low[i]])
        datas=pd.DataFrame(columns=columns, data=datas)  
        self.trend=trend(datas)

        position=self.trend.near_trend(self._close[0], self.date[0])
        if not self.position:
            if position == 'buy':
                self.order=self.buy()
            elif position == 'sell':
                self.order=self.sell()
        else:
            if position=='none':
                if self.position.size < 0:
                    # you are short
                    self.order=self.buy()
                elif self.position.size > 0:
                    # you are long
                    self.order=self.sell()
                