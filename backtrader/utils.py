from datetime import datetime
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from scipy.stats import zscore 
import numpy as np 
# import matplotlib.image as mpimg
# import matplotlib.pyplot as plt
# from IPython.display import Image

HEIGHT = 1000
WIDTH = 1500


def group_mean(df, key):
    '''
    grouping df by key (i.e. month=M, day=D) and return mean
    df: input dataframe 
    key: key to group 
    return: means of each item grouped 
    '''

    return(df.groupby(pd.Grouper(level='datetime', freq=key)).mean())


# def subset_sum(df, offset):
#     '''
#     calculate subset sum starting from next position until offset

#     '''
#      return df_price['price_usd_close'].iloc[item.name+1: item.name+offset].mean() - item['price_usd_close']


def one_day_from_df(df, date):
    '''
    extract one day data from dataframe
    df: input dataframe
    date: date to extract (i.e. 2020-04-1)
    return: one day (date) data as dataframe
    '''
    return(df.loc[date])

def mean_within_window(df, col, offset1=1, offset2=30):
    '''
    calculate mean of window (current, current + offset) items from dataframe
    '''
    # result = [df[col].iloc[row+offset1: row+offset2].mean() - df[col].iloc[row] for row in range(len(df))]
    return([df[col].iloc[row+offset1: row+offset2].mean() - df[col].iloc[row] for row in range(len(df))])


def mean_within_window_new(df, offset1=1, offset2=10):
    '''
    calculate mean of window (current, current + offset) items from dataframe
    '''
    # result = [df[col].iloc[row+offset1: row+offset2].mean() - df[col].iloc[row] for row in range(len(df))]
    return([df.iloc[row+offset1: row+offset2].mean() - df.iloc[row] for row in range(len(df))])

# in_date: string type
# return: datetime format  from('%Y-%m-%d %H:%M:%S' ) ==> to('%Y%m%dT%H%M%S')
def time_format_conversion(in_date):
    d = datetime.strptime(in_date, '%Y-%m-%d %H:%M:%S')
    return(d.strftime('%Y%m%dT%H%M%S'))



# merge two dataframes into one for data feeding 
def merge_price_signal(price, signal):
    return(pd.merge(price, signal, left_index=True, right_index=True))


def line_graph(x, y, title='y', graph_mode='lines+markers', height=HEIGHT, width=WIDTH):
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=x, y=y, mode=graph_mode, name=title))

    fig.update_layout(height=height, width=width)
    fig.show()


def line_graph_img(x, y, title='y', graph_mode='lines+markers', height=HEIGHT, width=WIDTH):
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=x, y=y, mode=graph_mode, name=title))

    fig.update_layout(height=height, width=width)
    fig.write_image('images/fig.png', engine='kaleido')
    # # img = mpimg.imread('images/fig.png')
    # Image(filename='images/fig.png')
    # # plt.imshow(img)


# graph_mode: lines, markers 
def multiline_graph(x, y1, y2, title=['y1', 'y2'], graph_mode='lines+markers', height=HEIGHT, width=WIDTH):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=x, y=y1, mode=graph_mode, name=title[0]), secondary_y=False)
    fig.add_trace(go.Scatter(x=x, y=y2, mode=graph_mode, name=title[1]), secondary_y=True)

    fig.update_layout(height=height, width=width)
    fig.show()


def multiline_graph_img(x, y1, y2, title=['y1', 'y2'], graph_mode='lines+markers', height=HEIGHT, width=WIDTH):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=x, y=y1, mode=graph_mode, name=title[0]), secondary_y=False)
    fig.add_trace(go.Scatter(x=x, y=y2, mode=graph_mode, name=title[1]), secondary_y=True)

    fig.update_layout(height=height, width=width)
    fig.write_image('images/fig.png', engine='kaleido')



def bar_graph_img(x, y,filename='images/fig.png'):
    '''
    draw bar graph image
    input: 
    return: image file (png)
    '''
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Bar(x, y))
    fig.write_image(filename, engine='kaleido')



def print_trade_analysis(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    #Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total,2)
    strike_rate = (total_won / total_closed) * 100
    #Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate','Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed,total_won,total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    #Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    #Print the rows
    print_list = [h1,r1,h2,r2]
    row_format ="{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('',*row))


def print_sqn(analyzer):
    sqn = round(analyzer.sqn,2)
    print('SQN: {}'.format(sqn))


def outliers_removal(df):
    z_scores = zscore(df)
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 3).all(axis=1)
    return(df[filtered_entries])
