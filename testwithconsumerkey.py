import json
import pandas as pd
from sqlalchemy import create_engine, desc, MetaData, Table

import requests
# from splinter import Browser
from config import td_consumer_key
import requests
import traceback

from exeptions import TDAAPIError


class tdbase:
    BASE = 'https://api.tdameritrade.com/v1/'
    _params = {'apikey': td_consumer_key}


class tdclientOptionshelper(tdbase):
    # endpoint = tdbase.BASE+"marketdata/chains"

    #################
    # OPTION CHAINS #
    #################
    # https://developer.tdameritrade.com/option-chains/apis
    from exeptions import TDAAPIError

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

    # def __init__(self):

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


class zerrolossstrategubuilder(tdclientOptionshelper):

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

    def singleOptionsDF(self,
                  symbol,
                  contractType='ALL',
                  strikeCount=-1,
                  includeQuotes=True,
                  strategy='ANALYTICAL',
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

        # return df[['putCall', 'symbol','strikePrice','mark','daysToExpiration','intrinsicValue','theoreticalOptionValue','bid','ask','bidSize','askSize','totalVolume','volatility','delta','gamma','theta','vega','rho','openInterest','timeValue','percentChange','markChange']]
        return df[
            ['putCall', 'symbol', 'strikePrice', 'mark', 'daysToExpiration', 'intrinsicValue', 'theoreticalOptionValue',
             'percentChange', 'markChange','bid','ask']]


    def strategy_calculate(self,row,shift,fee=5):
        call_sum_price = row['diff_call_mark{}'.format(shift)]
        put_sum_price= row['real_strategy_put_shifted_down_{}'.format(shift)]
        dif_strike_price= row['dif_strike_price{}'.format(shift)]
        day_to_experation= row['daysToExpiration']


        sum_of_strategy=(-(call_sum_price + put_sum_price))
        price_of_strategy=sum_of_strategy*100+fee
        persantage_of_strategy=(dif_strike_price*100-price_of_strategy)/(dif_strike_price*100)
        # full_profit_in_percentage_of_strategy=(dif_strike_price*100-strategy_price)/(dif_strike_price*100)
        reasonability_of_strategy=persantage_of_strategy-(day_to_experation/365*10)
        year_interest_of_strategy=persantage_of_strategy*365/day_to_experation

        return (sum_of_strategy,price_of_strategy,persantage_of_strategy,reasonability_of_strategy,year_interest_of_strategy)



    def getstrategyrowdataDF(self, symbol):
        df = self.singleOptionsDF(symbol)

        dfcalls = df.loc[df.putCall == 'CALL'][
            ['symbol', 'strikePrice', 'mark', 'daysToExpiration', 'bid', 'ask']]


        dfcalls = dfcalls.rename(
            columns={'symbol': 'callsymbol', 'mark': 'callmark', 'bid': 'callbid', 'ask': 'callask'})

        dfputts = df.loc[df.putCall == 'PUT'][
            ['symbol', 'strikePrice', 'mark', 'daysToExpiration', 'bid', 'ask']]
        dfputts = dfputts.reindex()
        dfputts = dfputts.rename(columns={'symbol': 'putsymbol', 'mark': 'putmark', 'bid': 'putbid', 'ask': 'putask'})

        dfmerged = pd.merge(dfcalls, dfputts, on=['strikePrice', 'daysToExpiration'])

        return dfmerged

    def getstrategycleaneddataDF(self,symbol,shifts=[1]):

        dfmerged=self.getstrategyrowdataDF(symbol)

        # delete 0 values puts and cals
        dfmerged = dfmerged[(dfmerged['putbid'] != 0) & (dfmerged['putask'] != 0) & (dfmerged['callbid'] != 0) & (
                    dfmerged['callask'] != 0)]


        return dfmerged



    def getstrategypreparedbasedataDF(self,symbol,shifts=[1],fee=5):

        dfmerged=self.getstrategycleaneddataDF(symbol)


        for shift in shifts:
            # calculate puts and strike  price shift 1 up in calculation
            dfmerged[['dif_strike_price{}'.format(shift), 'diff_call_mark{}'.format(shift)]] = \
            dfmerged.groupby('daysToExpiration')[
                ['strikePrice', 'callmark']].diff(periods=shift)

            # calculate calls price shift 1 down in calculation
            dfmerged[['diff_put_mark{}'.format(shift)]] = dfmerged.groupby('daysToExpiration')[['putmark']].diff(periods=(-(shift)))


            # for easy calculation shift puts down 1
            dfmerged['real_strategy_put_shifted_down_{}'.format(shift)] = dfmerged['diff_put_mark{}'.format(shift)].shift(
                (shift))


            dfmerged['sum_of_strategy{}'.format(shift)],\
            dfmerged['price_of_strategy{}'.format(shift)],\
            dfmerged[ 'persantage_of_strategy{}'.format(shift)],\
            dfmerged['reasonability_of_strategy{}'.format(shift)], \
            dfmerged['year_interest_of_strategy{}'.format(shift)] \
                        =zip(*dfmerged.apply(self.strategy_calculate, args=(shift,fee) ,axis=1))




        return dfmerged


    # def getstrategydata(self,symbol):
    #     df=self.singleOptionsDF(symbol)
    #
    #     dfcalls = df.loc[df.putCall == 'CALL'][
    #         ['symbol', 'strikePrice', 'mark', 'daysToExpiration', 'intrinsicValue', 'theoreticalOptionValue',
    #          'percentChange', 'markChange']]
    #
    #     dfcalls = dfcalls.rename(columns={'symbol': 'callsymbol', 'mark': 'callmark',
    #                                       'intrinsicValue': 'callintrinsicValue',
    #                                       'theoreticalOptionValue': 'calltheoreticalOptionValue','percentChange':'callpercentChange', 'markChange':'callmarkChange'})
    #
    #     dfputts = df.loc[df.putCall == 'PUT'][
    #         ['symbol', 'strikePrice', 'mark', 'daysToExpiration', 'intrinsicValue', 'theoreticalOptionValue',
    #          'percentChange', 'markChange']]
    #     dfputts=dfputts.reindex()
    #     dfputts = dfputts.rename(columns={'symbol': 'putsymbol', 'mark': 'putmark',
    #                                       'intrinsicValue': 'putintrinsicValue',
    #                                       'theoreticalOptionValue': 'puttheoreticalOptionValue','percentChange':'putpercentChange', 'markChange':'putmarkChange'})
    #
    #     return pd.merge(dfcalls, dfputts, on=['strikePrice','daysToExpiration'])



def testjsonrun():


    requester=zerrolossstrategubuilder()

    # recive option DF

    _symbol='MSFT'
    # _strategy="SINGLE"
    # _strategy="VERTICAL"
    _strategy="ANALYTICAL"
    _contractType='ALL'
    _includeQuotes=True
    filename="output_zerrowloss_{}_{}_{}.xlsx".format(_symbol,_strategy,_contractType)
    # dataDF = requester.optionsDF(symbol=_symbol.upper(), strategy=_strategy.upper(), #'VERTICAL',
    #                     includeQuotes= True,contractType=_contractType)
    # print(dataDF)
    # dataDF.to_excel(filename)

    dataDF = requester.singleOptionsDF(symbol=_symbol.upper(),strategy=_strategy.upper(),
                        includeQuotes= True,contractType=_contractType)
    print(dataDF)

    #to excel

    dataDF.to_excel(filename)

    #to DB

    engine = create_engine("sqlite:///:memory:")
    dataDF.to_sql(_symbol, engine,  if_exists="replace", index=False)
    # print(df.describe())
    metadata = MetaData()
    metadata.reflect(engine)
    # for table in metadata.tables.values():
    #     print(table.name)
    #     for column in table.c:
    #         print(column.name)

    ask=engine.execute("SELECT * FROM {}".format(_symbol)).fetchone()


    # print(ask)

    #  json

    datajson = requester.options(symbol=_symbol.upper(), strategy=_strategy.upper(),
                        contractType=_contractType)

    # print(json.dumps(datajson, indent=4, sort_keys=True))
    # print(datajson)


def teststrategy():
    requester = zerrolossstrategubuilder()

    _symbol = 'SAVA'
    filename = "output_zerrowloss_{}.xlsx".format(_symbol)

    # dataDF = requester.getstrategydata(symbol=_symbol.upper())
    dataDF = requester.getstrategypreparedbasedataDF(symbol=_symbol.upper())
    print(dataDF)

    dataDF.to_excel(filename)

if __name__ == '__main__':
    teststrategy()