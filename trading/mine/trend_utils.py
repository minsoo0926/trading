import pandas as pd
from utils import date_utils
import numpy as np
import matplotlib.pyplot as plt
import time

class trend:
    def __init__(self, data):
        end = 80
        start= 0
        max=local_max(data, start, end)
        min=local_min(data, start, end)
        
        z_max=np.polyfit(max['datetime'], max['high'],1)
        self.f_max=np.poly1d(z_max)
        z_min=np.polyfit(min['datetime'], min['low'],1)
        self.f_min=np.poly1d(z_min)

    def direction(self):
        if self.f_max[1]>0 and self.f_min[1]>0:
            return 'up'
        elif self.f_max[1]<0 and self.f_min[1]<0:
            return 'down'

    def near_trend(self, temp_price):
        if temp_price<(1.07)*self.f_min(time.time()) and self.direction()=='up':
            return 'buy'
        elif temp_price>(0.93)*self.f_max(time.time()) or self.direction()=='down':
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
    max_pts=[]
    time=[]
    for i in range(start, end-4):
        if data['high'][i]<data['high'][i+2] and data['high'][i+1]<data['high'][i+2] and data['high'][i+3]<data['high'][i+2] and data['high'][i+4]<data['high'][i+2]:
            max_pts.append([date_utils.str_to_utctimestamp(data['datetime'][i+2]),data['high'][i+2]])
    columns=['datetime', 'high']
    df=pd.DataFrame(data=max_pts, columns=columns)
    return df

def local_min(data, start, end):
    min_pts=[]
    time=[]
    for i in range(start, end-4):
        if data['low'][i]<data['low'][i+2] and data['low'][i+1]<data['low'][i+2] and data['low'][i+3]<data['low'][i+2] and data['low'][i+4]<data['low'][i+2]:
            min_pts.append([date_utils.str_to_utctimestamp(data['datetime'][i+2]),data['low'][i+2]])
    columns=['datetime', 'low']
    df=pd.DataFrame(data=min_pts, columns=columns)
    return df