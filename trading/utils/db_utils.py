from datetime import datetime 
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write.point import DEFAULT_WRITE_PRECISION 
from influxdb_client.client.write_api import SYNCHRONOUS
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

TOKEN = config['INFLUXDB']['API_KEY']
API_URL = config['INFLUXDB']['API_URL']
ORG = config['INFLUXDB']['ORG']
BUCKET = 'bucket'
DEFAULT_WRITE_PRECISION = WritePrecision.S

client = InfluxDBClient(url=API_URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
