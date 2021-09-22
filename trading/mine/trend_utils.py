import pandas as pd
from utils import date_utils
import numpy as np
import matplotlib.pyplot as plt
import time

class trend:
    def __init__(self, data):
        end = 34
        start= 0
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
        
        #converge
        elif self.f_max[1]<self.f_min[1]:
            return 'none'
        else:
            return 'none'


    def near_trend(self, temp_price):
        if (0.99)*self.f_min(time.time())<temp_price<(1.01)*self.f_min(time.time()) and self.direction()=='up':
            return 'buy'
        elif (1.01)*self.f_max(time.time())>temp_price>(0.99)*self.f_max(time.time()) and self.direction()=='down':
            return 'sell'
        else : 
            return 'none'   

    def graph(self, data):
        end=len(data)-1
        start=end-50 
        max=local_max(data, start, end)
        min=local_min(data, start, end)
        d=[]
        for x, y in zip(data['datetime'], data['close']):
            d.append([date_utils.str_to_utctimestamp(x), y])
        df=pd.DataFrame(data=d, columns=['datetime', 'close'])
        original_start=df.index[(df['datetime']==max['datetime'][0])].tolist()[0]
        original_end=df.index[(df['datetime']==max['datetime'][len(max)-1])].tolist()[0]
        df=df[original_start:original_end].reset_index(drop=True)
        plt.plot(df['datetime'], df['close'], 'k')

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
        plt.savefig('graph.png')


def local_max(data, start, end):
    max_pts=[]
    time=[]
    for i in range(start, end-4):
        if data['high'][i]<data['high'][i+2] and data['high'][i+1]<data['high'][i+2] and data['high'][i+3]<data['high'][i+2] and data['high'][i+4]<data['high'][i+2]:
            max_pts.append([date_utils.str_to_utctimestamp(data['datetime'][i+2]),data['high'][i+2]])
    max_pts.append([date_utils.str_to_utctimestamp(data['datetime'][end-1]),data['high'][end-1]])
    columns=['datetime', 'high']
    df=pd.DataFrame(data=max_pts, columns=columns)
    return df

def local_min(data, start, end):
    min_pts=[]
    time=[]
    for i in range(start, end-4):
        if data['low'][i]>data['low'][i+2] and data['low'][i+1]>data['low'][i+2] and data['low'][i+3]>data['low'][i+2] and data['low'][i+4]>data['low'][i+2]:
            min_pts.append([date_utils.str_to_utctimestamp(data['datetime'][i+2]),data['low'][i+2]])
    min_pts.append([date_utils.str_to_utctimestamp(data['datetime'][end-1]),data['low'][end-1]])
    columns=['datetime', 'low']
    df=pd.DataFrame(data=min_pts, columns=columns)
    return df
