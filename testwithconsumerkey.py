import json



import requests

# from splinter import Browser

# define an endpoint with a stock of your choice, MUST BE UPPER
from config import td_consumer_key

endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format('GOOG')

headers = {'apikey' : td_consumer_key}

# define the payload
payload = {'apikey' : td_consumer_key ,
           'periodType': 'day',
           'frequencyType': 'minute',
           'frequency': '1',
           'period': '2',
           'endDate': '1556158524000',
           'startDate': '1554535854000',
           'needExtendedHoursData': 'true'}

# make a request
content = requests.get(url=endpoint, params=payload)

# convert it dictionary object
data = content.json()

import time
import urllib
import requests



class tdclienthelper:
    BASE = 'https://api.tdameritrade.com/v1/'
    endpoint = BASE+"marketdata/chains"

    # def __init__(self):

    def payload_call(self,symbol):
        return {'apikey' : td_consumer_key,
                'symbol': symbol,
                'strategy': 'VERTICAL',
                'includeQuotes': 'TRUE',
                'contractType': 'CALL',
                'strikeCount': '-1'
                }
    def payload_put(self,symbol):
        return {'apikey' : td_consumer_key,
               'symbol': symbol,
               'strategy': 'VERTICAL',
               'includeQuotes': 'TRUE',
               'contractType': 'PUT',
               'strikeCount': '-1'
               }

    def getCallDataJson(self,symbol):
        content_call = requests.get(url=endpoint,
                                    params=self.payload_call(symbol))
        data_call = content_call.json()
        return data_call;

    def getPutDataJson(self,symbol):
        content_put = requests.get(url=endpoint, params=self.payload_put(symbol))
        data_put = content_put.json()

        return data_put;

    def getDataforSymvol(self,symvol):

        data_call = self.getCallDataJson(symvol)


        data_put = self.getPutDataJson(self,symvol)



code=tdclienthelper()
print(code.getCallDataJson("MSFT"))