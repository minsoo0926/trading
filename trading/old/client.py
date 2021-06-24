import websocket 
import requests
import threading
from datetime import datetime 
from json import loads, dumps 


BINANCE_SUBSCRIBE = '{ "method": "SUBSCRIBE", "params": [ "btcusdt@kline_1M"], "id": 1 }'
COINBASE_SUBSCRIBE = '{ "type": "subscribe", "product_ids": ["BTC-USD"], "channels": [ "ticker"] }'


class Client(threading.Thread):
    def __init__(self, url, exchange):
        super().__init__()
        self.ws = websocket.WebSocketApp(
            url = url, 
            on_message = self.on_message, 
            on_error = self.on_error, 
            on_close = self.on_close, 
            on_open = self.on_open 
        )

        self.exchange = exchange 

    
    def run(self):
        while True:
            self.ws.run_forever()

    
    def on_message(self, message):
        pass 

    def on_error(self, error):
        print(error)

    def on_close(self):
        print('### closed ###')

    def on_open(self):
        print(f'Connected to ')
        params = BINANCE_SUBSCRIBE
        ws.send(params)

    
    
# class Binance(Client):
#     # def __init__(self, url, exchange, tick, lock):
#     def __init__(self, url, exchange):

#         super().__init__(url, exchange)
#         print(f'{self.exchange} created')

#         # self.tick = tick[exchange]
#         # self.lock = lock
#         # self.updates = 0 
#         # self.last_update = tick 
    
#     def on_message(self, message):
#         data = loads(message)
#         # self.tick = data
    
#     def on_open(self):
#         super().on_open()
#         # params = BINANCE_SUBSCRIBE
#         # self.ws.send(dumps(params))


   


