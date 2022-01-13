import os
from configparser import ConfigParser

import pandas as pd

# from splinter import Browser
from td.client import TDClient
from tda.orders.common import Duration, OrderType, Destination, Session, OptionInstruction, ComplexOrderStrategyType
from tdameritrade.orders.constants import OrderStrategyType

# from config import td_consumer_key
import requests

from config.Util import get_project_root
from tdatrade.exeptions import TDAAPIError, GeneralError, ServerError, ExdLmtError, NotFndError, ForbidError, \
    TknExpError, NotNulError
from tdatrade.trade_strategy import TradeStrategy


class tdbase:
    fee=6
    BASE = 'https://api.tdameritrade.com/v1/'
    #
    # _params= {'apikey': td_consumer_key}
    def __init__(self,tdconsumer_key=None):
        # if tdconsumer_key is None:
        #     tdconsumer_key = td_consumer_key
        self._params = {'apikey': tdconsumer_key}


class tdclientOptionshelper(tdbase):
    # endpoint = tdbase.BASE+"marketdata/chains"

    #################
    # OPTION CHAINS #
    #################
    # https://developer.tdameritrade.com/option-chains/apis


    GET_OPTION_CHAIN = tdbase.BASE + 'marketdata/chains'  # GET
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
    STRATEGY_VALUES = (
    'SINGLE', 'ANALYTICAL', 'COVERED', 'VERTICAL', 'CALENDAR', 'STRANGLE', 'STRADDLE', 'BUTTERFLY', 'CONDOR',
    'DIAGONAL', 'COLLAR', 'ROLL')
    RANGE_VALUES = ('ITM', 'NTM', 'OTM', 'SAK', 'SBK', 'SNK', 'ALL')
    OPTION_TYPE_VALUES = ('S', 'NS', 'ALL')
    OPTION_EXPMONTH_VALUES = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'ALL')



    def options(self,
                symbol,
                contractType='ALL',
                strikeCount=-1,
                includeQuotes=True,
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
        params = self._params
        params.update({'symbol': symbol})
        # params = {'apikey' : td_consumer_key ,'symbol': symbol}

        if contractType not in self.CONTRACT_TYPE_VALUES:
            raise TDAAPIError('Contract type must be in {}'.format(self.CONTRACT_TYPE_VALUES))
        params['contractType'] = contractType

        if strikeCount:
            params['strikeCount'] = strikeCount

        params['includeQuotes'] = includeQuotes

        if strategy not in self.STRATEGY_VALUES:
            raise TDAAPIError('Strategy must be in {}'.format(self.STRATEGY_VALUES))

        params['strategy'] = strategy

        if interval:
            params['interval'] = interval

        if strike:
            params['strike'] = strike

        if range not in self.RANGE_VALUES:
            raise TDAAPIError('Range must be in {}'.format(self.RANGE_VALUES))
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

        if expMonth not in self.OPTION_EXPMONTH_VALUES:
            raise TDAAPIError('Expiration month must be in {}'.format(self.OPTION_EXPMONTH_VALUES))
        params['expMonth'] = expMonth

        if optionType not in self.OPTION_TYPE_VALUES:
            raise TDAAPIError('Option type must be in {}'.format(self.OPTION_TYPE_VALUES))

        return requests.get(self.GET_OPTION_CHAIN, params=params).json()

    def singleOptionsDF(self,
                  symbol,
                  contractType='ALL',
                  strikeCount=-1,
                  includeQuotes=True,
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
            # try:
            df[col] = pd.to_datetime(df[col], unit='ms')
            # except:
            #     # print(df,col)
            #     traceback.print_exc()
        # else:
        #     for date in dat['monthlyStrategyList']:
        #         # for strike in dat['callExpDateMap'][date]:
        #         #     ret.extend(dat['callExpDateMap'][date][strike])
        #         ret.extend(dat['callExpDateMap'])
        df = pd.DataFrame(ret)
        return df


    def getFee(self):
        return super().fee

# putCall                     -type of option
    # symbol                      - symvol
    # description
    # exchangeName                -exchange name
    # bid                         -bid
    # ask                         -ask
    # last
    # mark                        - price for strategy calculation
    # bidSize
    # askSize
    # bidAskSize
    # lastSize
    # highPrice
    # lowPrice
    # openPrice
    # closePrice
    # totalVolume                 -volume
    # tradeDate
    # tradeTimeInLong
    # quoteTimeInLong
    # netChange
    # volatility
    # delta                       -delta
    # gamma
    # theta
    # vega
    # rho
    # openInterest                -open interest
    # timeValue
    # theoreticalOptionValue      -teoretival value now
    # theoreticalVolatility
    # optionDeliverablesList
    # strikePrice                 -strike  price
    # expirationDate
    # daysToExpiration
    # expirationType
    # lastTradingDay
    # multiplier
    # settlementType
    # deliverableNote
    # isIndexOption
    # percentChange
    # markChange
    # markPercentChange
    # intrinsicValue
    # nonStandard
    # inTheMoney
    # mini
    # pennyPilot

    def sendOreder(self,account ,call_buy='SAVA_012822C54',call_buy_ammount=1.0,call_sell='SAVA_012822C55',call_sell_ammount=1.0, \
            put_buy='SAVA_012822P55',put_buy_ammount=1.0,put_sell='SAVA_012822P54',put_sell_ammount=1.0):
        tradeorder = TradeStrategy().set_complex_order_strategy_type(ComplexOrderStrategyType.IRON_CONDOR) \
            .set_duration(Duration.DAY) \
            .set_order_strategy_type(OrderStrategyType.SINGLE) \
            .set_order_type(OrderType.NET_DEBIT) \
            .copy_price(0.05) \
            .set_quantity(1.0) \
            .set_requested_destination(Destination.AUTO) \
            .set_session(Session.NORMAL) \
            .add_option_leg(OptionInstruction.BUY_TO_OPEN, call_buy, call_buy_ammount) \
            .add_option_leg(OptionInstruction.SELL_TO_OPEN, call_sell, call_sell_ammount) \
            .add_option_leg(OptionInstruction.BUY_TO_OPEN, put_buy, put_buy_ammount) \
            .add_option_leg(OptionInstruction.SELL_TO_OPEN, put_sell, put_sell_ammount)
        json_order=tradeorder.build()

        # make the request
        endpoint = tdbase.BASE +'accounts/{}/orders'.format(account)

        headers = self._headers(mode='json')

        data: dict = None

        # Define a new session.
        request_session = requests.Session()
        request_session.verify = True

        # Define a new request.
        request_request = requests.Request(
            method="POST",
            headers=headers,
            url=endpoint,
            params = self._params,
            data=data,
            json=json_order
        ).prepare()

        # Send the request.
        response: requests.Response = request_session.send(request=request_request)

        request_session.close()

        # grab the status code
        status_code = response.status_code

        # grab the response headers.
        response_headers = response.headers

        # Grab the order id, if it exists.
        if 'Location' in response_headers:
            order_id = response_headers['Location'].split('orders/')[1]
        else:
            order_id = ''

        # If it's okay and we need details, then add them.
        if response.ok :

            response_dict = {
                'order_id': order_id,
                'headers': response_headers,
                'content': response.content,
                'status_code': status_code,
                'request_body': response.request.body,
                'request_method': response.request.method
            }

            return response_dict

        # If it's okay and no details.
        elif response.ok:
            return response.json()

        else:

            if response.status_code == 400:
                raise NotNulError(message=response.text)
            elif response.status_code == 401:
                try:
                    self.grab_access_token()
                except:
                    raise TknExpError(message=response.text)
            elif response.status_code == 403:
                raise ForbidError(message=response.text)
            elif response.status_code == 404:
                raise NotFndError(message=response.text)
            elif response.status_code == 429:
                raise ExdLmtError(message=response.text)
            elif response.status_code == 500 or response.status_code == 503:
                raise ServerError(message=response.text)
            elif response.status_code > 400:
                raise GeneralError(message=response.text)



if __name__ == '__main__':
    # Grab configuration values.
    config = ConfigParser()
    CONFIG_PATH = os.path.join(get_project_root(), 'config/config.ini')  # requires `import os`
    config.read(CONFIG_PATH)

    CLIENT_ID = config.get('main', 'CLIENT_ID')
    REDIRECT_URI = config.get('main', 'REDIRECT_URI')
    CREDENTIALS_PATH = os.path.join(get_project_root(), config.get('main', 'JSON_PATH'))
    ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

    TDClient()




