from binance.client import AsyncClient
from binance import ThreadedWebsocketManager, BinanceSocketManager
import configparser
import asyncio
import json 


config = configparser.ConfigParser()
config.read('../config.ini')

API_KEY = config['BINANCE']['API_KEY']
SECRET_KEY = config['BINANCE']['SECRET_KEY']
API_URL = config['BINANCE']['API_URL']


async def main():
    client = await AsyncClient.create()
    # client = AsyncClient.create(api_key=API_KEY, api_secret=SECRET_KEY)
    res = await client.get_exchange_info()
    print(json.dumps(res, indent=4))

    await client.close_connection()


#loop = asyncio.get_event_loop()
#loop.run_until_complete(main())



def main1():

    symbol = 'BNBBTC'

    twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=SECRET_KEY)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        print(f"message type: {msg['e']}")
        print(msg)

    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)
    streams = ['BNBBTC@miniTicker', 'BNBBTC@bookTicker']
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)


async def main2():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.symbol_ticker_socket('BTCUSDT')
    # ts = bm.trade_socket('BTCUSDT')

    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)

    await client.close_connection()

#

loop = asyncio.get_event_loop()
loop.run_until_complete(main2())