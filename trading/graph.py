import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from mine import trend_utils
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import date_utils
import ccxt
import matplotlib

%matplotlib tk

HEIGHT = 1000
WIDTH = 1500

def line_graph(x, y, title='y', graph_mode='lines+markers', height=HEIGHT, width=WIDTH):
    '''
    draw line graph
    x: x axis data
    y: y axis data
    title: graph title 
    graph_mode: lines, markers, lines+markers 
    height:
    width 
    '''

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=x, y=y, mode=graph_mode, name=title))

    fig.update_layout(height=height, width=width)
    fig.show()


def line_graph_img(x, y, title='y', graph_mode='lines+markers', height=HEIGHT, width=WIDTH, filename='images/fig.png'):
    '''
    draw line graph and save as an image file 
    x: x axis data
    y: y axis data
    title: graph title 
    graph_mode: lines, markers, lines+markers 
    height:
    width 
    filename: default = 'images/fig.png'
    '''

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=x, y=y, mode=graph_mode, name=title))

    fig.update_layout(height=height, width=width)
    fig.write_image(filename, engine='kaleido')
    # # img = mpimg.imread('images/fig.png')
    # Image(filename='images/fig.png')
    # # plt.imshow(img)


# graph_mode: lines, markers 
def multiline_graph(x, y1, y2, title=['y1', 'y2'], graph_mode='lines+markers', height=HEIGHT, width=WIDTH):
    '''
    draw multi-line graph 
    x: x axis data
    y_list: list of y axes data
    title: graph title 
    graph_mode: lines, markers, lines+markers 
    height:
    width 
    '''

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=x, y=y1, mode=graph_mode, name=title[0]), secondary_y=False)
    fig.add_trace(go.Scatter(x=x, y=y2, mode=graph_mode, name=title[1]), secondary_y=True)

    fig.update_layout(height=height, width=width)
    fig.show()


def multiline_graph_img(x, y1, y2, title=['y1', 'y2'], graph_mode='lines+markers', height=HEIGHT, width=WIDTH, filename='images/fig.png'):
    '''
    draw multi-line graph and save as an image file 
    x: x axis data
    y_list: list of y axes data
    title: graph title 
    graph_mode: lines, markers, lines+markers 
    height:
    width:
    filename: default = 'images/fig.png'
    '''

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=x, y=y1, mode=graph_mode, name=title[0]), secondary_y=False)
    fig.add_trace(go.Scatter(x=x, y=y2, mode=graph_mode, name=title[1]), secondary_y=True)

    fig.update_layout(height=height, width=width)
    fig.write_image(filename, engine='kaleido')



def bar_graph_img(x, y,filename='images/fig.png'):
    '''
    draw bar graph image
    input: 
    return: image file (png)
    '''
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Bar(x, y))
    fig.write_image(filename, engine='kaleido')

if __name__=="__main__":
    df1 = pd.read_csv('/root/trading/trading/data/20200101-ETH_future.csv')
    binance = ccxt.binance()
    eth = binance.fetch_ticker("ETH/USDT")

    a = trend_utils.trend(df1[len(df1)-34:len(df1)].reset_index(drop=True))
    print(a.near_trend(eth['close']))
    a.graph(df1)

    