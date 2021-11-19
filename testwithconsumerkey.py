import json
import pandas as pd


import requests

# from splinter import Browser

# define an endpoint with a stock of your choice, MUST BE UPPER
from tdameritrade.exceptions import TDAAPIError

from config import td_consumer_key
BASE = 'https://api.tdameritrade.com/v1/'

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

#################
# OPTION CHAINS #
#################
# https://developer.tdameritrade.com/option-chains/apis
GET_OPTION_CHAIN = BASE + 'marketdata/chains'  # GET
OPTION_CHAIN_ARGS = ('symbol',
                     'contractType',
                     'strikeCount',
                     'includeQuotes',
                     'strategy',
                     'interval',
                     'strike',
                     'range',
                     'fromDate',
                     'toDate',
                     'volatility',
                     'underlyingPrice',
                     'interestRate',
                     'daysToExpiration',
                     'expMonth',
                     'optionType')
CONTRACT_TYPE_VALUES = ('CALL', 'PUT', 'ALL')
STRATEGY_VALUES = ('SINGLE', 'ANALYTICAL', 'COVERED', 'VERTICAL', 'CALENDAR', 'STRANGLE', 'STRADDLE', 'BUTTERFLY', 'CONDOR', 'DIAGONAL', 'COLLAR', 'ROLL')
RANGE_VALUES = ('ITM', 'NTM', 'OTM', 'SAK', 'SBK', 'SNK', 'ALL')
OPTION_TYPE_VALUES = ('S', 'NS', 'ALL')
OPTION_EXPMONTH_VALUES = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'ALL')




class tdclienthelper:
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


    def options(self,
                symbol,
                contractType='ALL',
                strikeCount=-1,
                includeQuotes=False,
                strategy='SINGLE',
                interval=None,
                strike=None,
                range='ALL',
                fromDate=None,
                toDate=None,
                volatility=None,
                underlyingPrice=None,
                interestRate=None,
                daysToExpiration=None,
                expMonth='ALL',
                optionType='ALL'):
        '''request option chain information

        Args:
            symbol (str): Enter one symbol
            contractType (str): Type of contracts to return in the chain. Can be CALL, PUT, or ALL. Default is ALL.
            strikeCount (int): The number of strikes to return above and below the at-the-money price.
            includeQuotes (bool): Include quotes for options in the option chain. Can be TRUE or FALSE. Default is FALSE.
            strategy (str): Passing a value returns a Strategy Chain. Possible values are SINGLE, ANALYTICAL (allows use of the volatility, underlyingPrice, interestRate, and daysToExpiration params to calculate theoretical values), COVERED, VERTICAL, CALENDAR, STRANGLE, STRADDLE, BUTTERFLY, CONDOR, DIAGONAL, COLLAR, or ROLL. Default is SINGLE.
            interval (int): Strike interval for spread strategy chains (see strategy param).
            strike (float): Provide a strike price to return options only at that strike price.
            range (str): Returns options for the given range. Possible values are:
                            ITM: In-the-money
                            NTM: Near-the-money
                            OTM: Out-of-the-money
                            SAK: Strikes Above Market
                            SBK: Strikes Below Market
                            SNK: Strikes Near Market
                            ALL: All Strikes
                            Default is ALL.
            fromDate (str): Only return expirations after this date. For strategies, expiration refers to the nearest term expiration in the strategy. Valid ISO-8601 formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz.
            toDate (str): Only return expirations before this date. For strategies, expiration refers to the nearest term expiration in the strategy. Valid ISO-8601 formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz.
            volatility (float): Volatility to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param).
            underlyingPrice (float): Underlying price to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param).
            interestRate (float): Interest rate to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param).
            daysToExpiration (int): Days to expiration to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param).
            expMonth (str): Return only options expiring in the specified month. Month is given in the three character format.
                                Example: JAN
                                Default is ALL.
            optionType (str): Type of contracts to return. Possible values are:
                                S: Standard contracts
                                NS: Non-standard contracts
                                ALL: All contracts
                                Default is ALL.
        '''
        params = {'apikey' : td_consumer_key ,'symbol': symbol}

        if contractType not in CONTRACT_TYPE_VALUES:
            raise TDAAPIError('Contract type must be in {}'.format(CONTRACT_TYPE_VALUES))
        params['contractType'] = contractType

        if strikeCount:
            params['strikeCount'] = strikeCount

        params['includeQuotes'] = includeQuotes

        if strategy not in STRATEGY_VALUES:
            raise TDAAPIError('Strategy must be in {}'.format(STRATEGY_VALUES))

        params['strategy'] = strategy

        if interval:
            params['interval'] = interval

        if strike:
            params['strike'] = strike

        if range not in RANGE_VALUES:
            raise TDAAPIError('Range must be in {}'.format(RANGE_VALUES))
            params['range'] = range

        if fromDate:
            params['fromDate'] = fromDate

        if toDate:
            params['toDate'] = toDate

        if strategy == 'ANALYTICAL':
            if volatility:
                params['volatility'] = volatility
            if underlyingPrice:
                params['underlyingPrice'] = underlyingPrice
            if interestRate:
                params['interestRate'] = interestRate
            if daysToExpiration:
                params['daysToExpiration'] = daysToExpiration

        if expMonth not in OPTION_EXPMONTH_VALUES:
            raise TDAAPIError('Expiration month must be in {}'.format(OPTION_EXPMONTH_VALUES))
        params['expMonth'] = expMonth

        if optionType not in OPTION_TYPE_VALUES:
            raise TDAAPIError('Option type must be in {}'.format(OPTION_TYPE_VALUES))

        return requests.get(GET_OPTION_CHAIN, params=params).json()

    def optionsDF(self,
                  symbol,
                  contractType='ALL',
                  strikeCount=-1,
                  includeQuotes=False,
                  strategy='SINGLE',
                  interval=None,
                  strike=None,
                  range='ALL',
                  fromDate=None,
                  toDate=None,
                  volatility=None,
                  underlyingPrice=None,
                  interestRate=None,
                  daysToExpiration=None,
                  expMonth='ALL',
                  optionType='ALL'):
        '''return options chain as dataframe'''
        ret = []
        dat = self.options(symbol=symbol,
                           contractType=contractType,
                           strikeCount=strikeCount,
                           includeQuotes=includeQuotes,
                           strategy=strategy,
                           interval=interval,
                           strike=strike,
                           range=range,
                           fromDate=fromDate,
                           toDate=toDate,
                           volatility=volatility,
                           underlyingPrice=underlyingPrice,
                           interestRate=interestRate,
                           daysToExpiration=daysToExpiration,
                           expMonth=expMonth,
                           optionType=optionType)
        for date in dat['callExpDateMap']:
            for strike in dat['callExpDateMap'][date]:
                ret.extend(dat['callExpDateMap'][date][strike])
        for date in dat['putExpDateMap']:
            for strike in dat['putExpDateMap'][date]:
                ret.extend(dat['putExpDateMap'][date][strike])

        df = pd.DataFrame(ret)
        for col in ('tradeTimeInLong', 'quoteTimeInLong',
                    'expirationDate', 'lastTradingDay'):
            df[col] = pd.to_datetime(df[col], unit='ms')

        return df


    def getCallDataJson(self,symbol):
        content_call = requests.get(url=endpoint,
                                    params=self.payload_call(symbol))
        data_call = content_call.json()
        return data_call;

    def getPutDataJson(self,symbol):
        content_put = requests.get(url=endpoint, params=self.payload_put(symbol))
        data_put = content_put.json()
        return data_put

    def getCallDataJsonDF(self, symbol):

        data_call = self.getPutDataJson(symbol)

        return pd.json_normalize(data_call)


    def getPutDataJsonDF(self, symbol):
        data_put = self.getPutDataJson(symbol)


        return pd.json_normalize(data_put)



    def getDataforSymvol(self,symvol):

        data_call = self.getCallDataJson(symvol)
        data_put = self.getPutDataJson(self,symvol)

    def calculatecustom4strategy(self,data_call,data_put):

        for stridx, stratery in enumerate(data_call['monthlyStrategyList']):
            daysToExp = int(stratery['daysToExp'])
            print(daysToExp)
            for optidx, option in enumerate(stratery['optionStrategyList']):
                call_primar = option['primaryLeg']['symbol']
                call_secondary = option['secondaryLeg']['symbol']
                primar_strike = float(option['primaryLeg']['strikePrice'])
                secondary_strike = float(option['secondaryLeg']['strikePrice'])
                call_strike = option['strategyStrike']
                call_bid = float(option['strategyBid'])
                call_ask = float(option['strategyAsk'])
                put_bid = float(data_put['monthlyStrategyList'][stridx]['optionStrategyList'][optidx]['strategyBid'])
                put_ask = float(data_put['monthlyStrategyList'][stridx]['optionStrategyList'][optidx]['strategyAsk'])
                mark = round((call_bid + call_ask) / 2, 2)
                m = round((put_bid + put_ask) / 2, 2)
                res = round(m + mark, 2)
                spread = secondary_strike - primar_strike
                if (call_bid > 0.0 and call_ask > 0.0 and put_bid > 0.0 and put_ask > 0.0 and res < spread):
                    profit = round((spread - res) / spread * 100, 1) - daysToExp * 0.027
                    # print(' {} : {} - {} | {} | {} | {} - {} | {} = {} ? {} +{}%'.format( call_primar,call_strike,call_bid,call_ask,put_bid,put_ask,mark,m,res,spread,profit))






code=tdclienthelper()
data = code.options('MSFT',strategy='VERTICAL',
                    includeQuotes= True,contractType='CALL'
)
print(data)

df=pd.json_normalize(data)
print(df)

#
# print(code.getCallDataJsonDF("MSFT"))