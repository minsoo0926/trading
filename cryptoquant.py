import requests
import configparser
from urllib.parse import urljoin 

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['CRYPTOQUANT']['API_KEY']
API_URL = config['CRYPTOQUANT']['API_URL']


headers = {'Authorization': 'Bearer ' + API_KEY}
params = {'type': 'exchange'}

PATH = 'btc/status/entity-list'
URL = urljoin(API_URL, PATH)

print(URL)
response = requests.get(URL, headers=headers, params=params)
print(type(response))


