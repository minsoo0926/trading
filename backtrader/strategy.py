
import backtrader as bt
import btalib
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

size = 1
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


HIGH_GAP = 100
LOW_GAP = -70


# signal: long_signal, short_signal, long_exit, short_exit 

class PriceData(btfeeds.PandasData):
    params = (
        ('dtformat', DATE_FORMAT),
        ('datetime', None),
        # ('datetime', 'datetime'),
        ('open', 'price_usd_open'),
        ('high', 'price_usd_high'),
        ('low', 'price_usd_low'),
        ('close', 'price_usd_close'),
        ('openinterest', None),
    )

class PriceSignalData(btfeeds.PandasData):
    lines = ('gap', 'index', )
    params = (
        ('dtformat', DATE_FORMAT),
        ('datetime', None),
        # ('datetime', 'datetime'),
        ('open', 'price_usd_open'),
        ('high', 'price_usd_high'),
        ('low', 'price_usd_low'),
        ('close', 'price_usd_close'),
        ('openinterest', None),
        ('gap', 'coinbase_premium_gap'),
        ('index', 'coinbase_premium_index'),

    )


class CoinbaseData(btfeeds.PandasData):
    params = (
        ('dtformat', DATE_FORMAT),
        ('datetime', None),
        ('gap', 'coinbase_premium_gap'),
        ('index', 'coinbase_premium_index'),
        ('open', None),
        ('high', None),
        ('low', None),
        ('close', None),
        ('openinterest', None),
    )




class PrintData(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        # print('open:', self.data.open[0], 'high:', self.data.high[0], 'low:', self.data.low[0], 'close:', self.data.close[0])
        # print(self.datas[0].datetime.date(0), self.datas[0].datetime.time(0),  'open:', self.datas[0].open[0], 'high:', self.datas[0].high[0], 'low:', self.datas[0].low[0], 'close:', self.datas[0].close[0])
        print(self.datas[0].datetime.date(0), self.datas[0].datetime.time(0), self.datas[0].gap[0], self.datas[0].index[0])


# class PrintClose(bt.Strategy):
#     def __init__(self):
#         self.dataclose = self.datas[0].close
       
#     def log(self, txt, dt=None):
#         # dt = self.dataclose[0]
#         dt = dt or self.datas[0].datetime.date(0)
#         # print('1', self.datas[0].datetime.date(0), self.datas[0].datetime.time(0), self.data.close[0], txt)
#         print('2', self.data.datetime.date(0), self.data.datetime.time(0), self.data.close[0], txt)

#     def next(self):
#         self.log('Close', self.dataclose[0])
#         cerebro = bt.Cerebro()



class SMACross(bt.SignalStrategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=5,  # period for the fast moving average
        pslow=30  # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        # sma1 = btalib.sma(price, period=self.p.pfast)
        # sma1 = bt.indicators.MovingAverageSimple(period=self.params.pfast)
        #sma2 = btalib.sma(price, period=self.p.pslow)
        crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        # self.crossover = btalib.crossover(sma1, sma2)  # crossover signal
        # self.holding = 0
        self.signal_add(bt.SIGNAL_LONG, crossover)

    # def next(self):
    #     # current_stock_price = self.data.close[0]

    #     if not self.position:  # not in the market
    #         if self.sma1 > 0:  # if fast crosses slow to the upside
    #             # available_stocks = self.broker.getcash() / current_stock_price
    #             self.buy(size=size)
    #             print('BUY:(', self.sma1[0], ')', self.datas[0].datetime.date(0), self.datas[0].datetime.time(0), self.dataclose[0])

    #     elif self.sam1 < 0:  # in the market & cross to the downside
    #         self.close()  # close long position

    # def notify_order(self, order):
    #     if order.status not in [order.Completed]:
    #         return

    #     if order.isbuy():
    #         action = 'Buy'
    #     elif order.issell():
    #         action = 'Sell'

    #     stock_price = self.data.close[0]
    #     cash = self.broker.getcash()
    #     value = self.broker.getvalue()
    #     self.holding += order.size

    #     print('%s[%d] holding[%d] price[%d] cash[%.2f] value[%.2f]'
    #           % (action, abs(order.size), self.holding, stock_price, cash, value))



class RSI(bt.Strategy):

    parmas = dict(
        rsi_periods = 14,
        rsi_upper = 70,
        rsi_lower = 30,
        rsi_mid = 50 
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.rsi = btind.RSI_SMA(self.data.close, period=10)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy(size=size)
                cost_profit = self.dataclose[0] * size
                print('BUY:(', self.rsi[0], ')', self.datas[0].datetime.date(0), self.datas[0].datetime.time(0), self.dataclose[0], 'cost (profit): ', cost_profit)
        else:
            if self.rsi > 70:
                self.sell(size=size)
                print('SELL:(', self.rsi[0], ')', self.datas[0].datetime.date(0), self.datas[0].datetime.time(0), self.datas[0].close[0], 'cost (profit): ', cost_profit)
    
    def log(self, txt, dt=None):
        print(txt, dt)



class MACrossOver(bt.SignalStrategy):
    alias = ('SMACrossOver', )

    params = (
        ('fast', 20),
        ('slow', 200),
        ('exitbars', 1),
        ('_movav', bt.ind.MovAv.SMA)
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None 

        sma_fast = self.p._movav(period=self.p.fast)
        sma_slow = self.p._movav(period=self.p.slow)

        self.buysig = bt.ind.CrossOver(sma_fast, sma_slow)
        self.sellsig = bt.ind.CrossOver(sma_slow, sma_fast)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' % (order.executed.price, order.executed.value, order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' % (order.executed.price, order.executed.value, order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))        
        
    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        
        # Check if we are in the market
        if not self.position:
        
            # buy signal
            if self.buysig > 0:
                # BUY
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
            elif self.sellsig > 0:
                #if len(self) >= (self.bar_executed + self.params.exitbars):
                    # Sell
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                    # Keep track of the created order to avoid a 2nd order
                # self.order = self.sell(size=1)
                self.order = self.sell()

                #else:
                    #return
            else:
                return
        else:    # in a position        
            if self.buysig < 0:
                # Buy Closed
                self.log('BUY CLOSE, %.2f' % self.dataclose[0])
                self.order = self.close()
                self.order = self.sell()
                # self.order = self.sell(size=1)

            # elif ignore zero case
            elif self.sellsig < 0:
                # Sell Closed
                self.log('SELL CLOSE, %.2f' % self.dataclose[0])
                self.order = self.close()
                self.order = self.buy()
            else:
                return



class Test(bt.Strategy):

    def __init__(self):
        # self.dataclose = self.datas[0].close
        self.gap = self.datas[0].gap 
        self.index = self.datas[0].index
        self.close = self.datas[0].close  
        self.sma = btind.SimpleMovingAverage(self.datas[0].close, period=20)
        self.ema = btind.ExponentialMovingAverage(self.datas[0].close, period=20)
        self.rsi = btind.RSI_SMA(self.close, period=20)
        self.close_sma_diff = self.data.close - self.sma
        self.price_over_sma = self.close > self.sma 
        # self.premium = btalib.sma(self.datas.index)
        # print(self.gap[0])
        self.buy_sig = bt.And(self.price_over_sma, self.close_sma_diff > 0)
        bt.LinePlotterIndicator(self.buy_sig, name='Buy Signal')

        # print(f'init: item')
        # for item in self.rsi:
        #     print(item) 


    def next(self):
        # print('Data Feed: ', '(', self.gap[0], ')', self.datas[0].datetime.date(0), self.datas[0].datetime.time(0), self.datas[0].close[0])
        print(f'Feed - {self.datas[0].datetime.date(0)}, {self.datas[0].datetime.time(0)} ({self.gap[0]}): {self.datas[0].close[0]:.2f}, (s: {self.sma[0]:.2f} d: {self.close_sma_diff[0]:.2f} c: {self.price_over_sma[0]!s} e: {self.ema[0]:.2f}  b: {self.buy_sig[0]} r: {self.rsi[0]:.2f})')

        # print(f'position: {self.position.size}, gap: {self.gap[0]}')
        # if not self.position:
        #     if self.gap[0] > 100:
        #         self.buy(size=size)
        #         # print('BUY:(', self.gap[0], ')', self.datas[0].datetime.date(0), self.datas[0].datetime.time(0), self.datas[0].close[0])
        #         print('BUY:(', self.gap[0], ')')

        # else:
        #     if self.gap[0] < -100:
        #         self.sell(size=size)
        #         # print('SELL:(', self.gap[0], ')', self.datas[0].datetime.date(0), self.datas[0].datetime.time(0), self.datas[0].close[0])
        #         print('SELL:(', self.gap[0], ')')


        # liquidation need to be considered.... : check orders for liquidation 




        # # FIRST STRATEGY
        # if not self.position:
        #     if (self.gap[-1] > HIGH_GAP and increasing(self.gap[0] + self.datas[0].close[0], self.gap[-1] + self.datas[0].close[-1]) and increasing(self.gap[0], self.gap[-1])):
        #         self.buy(size=size)
        #         print(f'BUY ORDER:( {self.gap[0]})')
        #     elif (self.gap[-1] < LOW_GAP and decreasing(self.gap[0] + self.datas[0].close[0], self.gap[-1] + self.datas[0].close[-1]) and decreasing(self.gap[0], self.gap[-1])):
        #         self.sell(size=size)
        #         print(f'SELL ORDER:( {self.gap[0]})')


        #     # if self.gap[0] > HIGH_GAP:
        #     #     self.buy(size=size)
        #     #     # print('BUY:(', self.gap[0], ')', self.datas[0].datetime.date(0), self.datas[0].datetime.time(0), self.datas[0].close[0])
        #     #     print(f'BUY:( {self.gap[0]})')
        #     # elif self.gap[0] < LOW_GAP:
        #     #     self.sell(size=size)
        #     #     # print('SELL:(', self.gap[0], ')', self.datas[0].datetime.date(0), self.datas[0].datetime.time(0), self.datas[0].close[0])
        #     #     print(f'SELL:( {self.gap[0]})')

        # else:
        #     if self.position.size > 0:
        #         # sell 
        #         if (self.gap[-1] < LOW_GAP and decreasing(self.gap[0] + self.datas[0].close[0], self.gap[-1] + self.datas[0].close[-1]) and decreasing(self.gap[0], self.gap[-1])):
        #             self.sell(size=size)
        #             print(f'SELL ORDER:( {self.gap[0]})')
        #     else: 
        #         # buy 
        #         if (self.gap[-1] > HIGH_GAP and increasing(self.gap[0] + self.datas[0].close[0], self.gap[-1] + self.datas[0].close[-1]) and increasing(self.gap[0], self.gap[-1])):
        #             self.buy(size=size)
        #             print(f'BUY ORDER:( {self.gap[0]})')


        # # SECOND STRATEGY
        if not self.position:
            if (self.gap[-1] > HIGH_GAP and increasing(self.gap[0] + self.datas[0].close[0], self.gap[-1] + self.datas[0].close[-1]) and increasing(self.gap[0], self.gap[-1])):
                self.buy(size=size)
                print(f'BUY ORDER:( {self.gap[0]})')


        else:
            if  (self.gap[-1] < LOW_GAP and decreasing(self.gap[0] + self.datas[0].close[0], self.gap[-1] + self.datas[0].close[-1]) and decreasing(self.gap[0], self.gap[-1])):
                    self.sell(size=size)
                    print(f'SELL ORDER:( {self.gap[0]})')

        # if self.price_over_sma == True:
        #     print('True')
        # else: 
        #     print('False')


    # def notify_order(self, order):
    #     if order.status == order.Completed:
    #         print(self.getposition(order.data).price) # (abs(order.executed.value) + order.executed.comm) / abs(order.executed.size))

    
    def notify_order(self, order):
        # 1. If order is submitted/accepted, do nothing
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 2. If order is buy/sell executed, report price executed
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f'BUY EXECUTED, Price: {order.executed.price:8.2f}, Size: {order.executed.size:8.2f} Cost: {order.executed.value:8.2f}, Comm: {order.executed.comm:8.2f}')

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

                print(f'p: {self.getposition(order.data).price} s: {self.getposition(order.data).size}') # ' c: {self.getposition(order.data).comm}')
                # print(f'position: {self.getposition(order.data)}') # position: size, price, price orig, closed, opened, adjbase 


            else:
                print(f'SELL EXECUTED, Price: {order.executed.price:8.2f}, Size: {order.executed.size:8.2f} Cost: {order.executed.value:8.2f}, Comm: {order.executed.comm:8.2f}')
                # print('SELL EXECUTED, {0:8.2f}, Size: {1:8.2f} Cost: {2:8.2f}, Comm{3:8.2f}'.format(
                #     order.executed.price,
                #     order.executed.size,
                #     order.executed.value,
                #     order.executed.comm))

            self.bar_executed = len(self)  # when was trade executed
        # 3. If order is canceled/margin/rejected, report order canceled
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        print('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))


    def log(self, txt, dt=None):
        print(txt, dt)


def decreasing(current, previous):
    return(current < previous)

def increasing(current, previous):
    return(current > previous)


# c vs b: (c:d, b:d), (c:d, b:i), (c:i, b:d), (c:i, b:i)