import pandas as pd

from tda.tddataprovider import tdclientOptionshelper


class zerroloss_strategy_TD_estimator(tdclientOptionshelper):
    def __init__(self,symbol,shifts=[1],tdconsumer_key=None):
        self.symbol=symbol
        self.shifts=shifts
        super(tdclientOptionshelper, self).__init__(tdconsumer_key)
        # self.fee=tdclientOptionshelper.getFee()

    def td_singleOptionsDF(self,tdmarket_data):
        '''return options chain as dataframe'''
        ret = []

        for date in tdmarket_data['callExpDateMap']:
            for strike in tdmarket_data['callExpDateMap'][date]:
                ret.extend(tdmarket_data['callExpDateMap'][date][strike])
        for date in tdmarket_data['putExpDateMap']:
            for strike in tdmarket_data['putExpDateMap'][date]:
                ret.extend(tdmarket_data['putExpDateMap'][date][strike])

        df = pd.DataFrame(ret)

        # return df[['putCall', 'symbol','strikePrice','mark','daysToExpiration','intrinsicValue','theoreticalOptionValue','bid','ask','bidSize','askSize','totalVolume','volatility','delta','gamma','theta','vega','rho','openInterest','timeValue','percentChange','markChange']]
        return df[
            ['putCall', 'symbol', 'strikePrice', 'mark', 'daysToExpiration', 'intrinsicValue', 'theoreticalOptionValue',
             'percentChange', 'markChange','bid','ask']]


    def strategy_calculate(self,row,shift):
        call_sum_price = row['diff_call_mark{}'.format(shift)]
        put_sum_price= row['real_strategy_put_shifted_down_{}'.format(shift)]
        dif_strike_price= row['dif_strike_price{}'.format(shift)]
        day_to_experation= row['daysToExpiration']


        sum_of_strategy=call_sum_price + put_sum_price
        cost_of_margine = (1 * day_to_experation / 365 )*12/100

        if sum_of_strategy == 0 :
            total_profit_loss =0
            persantage_of_strategy = 0
        else:
            total_profit_loss = dif_strike_price + sum_of_strategy - super().getFee() / 100 - cost_of_margine
            persantage_of_strategy = -total_profit_loss/sum_of_strategy

        year_interest_of_strategy=persantage_of_strategy*365/day_to_experation


        return (sum_of_strategy,cost_of_margine,total_profit_loss,persantage_of_strategy,year_interest_of_strategy)



    def getstrategyrowdataDF(self,tdmarket_data):


        dfcalls = tdmarket_data.loc[tdmarket_data.putCall == 'CALL'][
            ['symbol', 'strikePrice', 'mark', 'daysToExpiration', 'bid', 'ask']]


        dfcalls = dfcalls.rename(
            columns={'symbol': 'callsymbol', 'mark': 'callmark', 'bid': 'callbid', 'ask': 'callask'})

        dfputts = tdmarket_data.loc[tdmarket_data.putCall == 'PUT'][
            ['symbol', 'strikePrice', 'mark', 'daysToExpiration', 'bid', 'ask']]
        dfputts = dfputts.reindex()
        dfputts = dfputts.rename(columns={'symbol': 'putsymbol', 'mark': 'putmark', 'bid': 'putbid', 'ask': 'putask'})

        dfmerged = pd.merge(dfcalls, dfputts, on=['strikePrice', 'daysToExpiration'])

        return dfmerged

    def getstrategycleaneddataDF(self,tdmarket_data):

        # delete 0 values puts and cals
        dfmerged = tdmarket_data[(tdmarket_data['putbid'] != 0) & (tdmarket_data['putask'] != 0) & (tdmarket_data['callbid'] != 0) & (
                    tdmarket_data['callask'] != 0)]


        return dfmerged

    def getstrategypreparedbasedataDF(self,tdmarket_data_json):
        # make dataframe from json
        tdmarket_data=self.td_singleOptionsDF(tdmarket_data_json)
        #merge calls and puts to strategu
        tdmarket_data=self.getstrategyrowdataDF(tdmarket_data)

        tdmarket_data=self.getstrategycleaneddataDF(tdmarket_data)

        # print(tdmarket_data)


        for shift in self.shifts:
            # calculate puts and strike  price shift 1 up in calculation
            tdmarket_data[['dif_strike_price{}'.format(shift), 'diff_call_mark{}'.format(shift)]] = \
            tdmarket_data.groupby('daysToExpiration')[
                ['strikePrice', 'callmark']].diff(periods=shift)

            # calculate calls price shift 1 down in calculation
            tdmarket_data[['diff_put_mark{}'.format(shift)]] = tdmarket_data.groupby('daysToExpiration')[['putmark']].diff(periods=(-(shift)))


            # for easy calculation shift puts down 1
            tdmarket_data['real_strategy_put_shifted_down_{}'.format(shift)] = tdmarket_data['diff_put_mark{}'.format(shift)].shift(
                (shift))

            tdmarket_data['sum_of_strategy{}'.format(shift)],\
            tdmarket_data['cost_of_margine_of_strategy{}'.format(shift)],\
            tdmarket_data[ 'total_profit_loss_of_strategy{}'.format(shift)],\
            tdmarket_data['persantage_of_strategy{}'.format(shift)], \
            tdmarket_data['year_interest_of_strategy{}'.format(shift)] \
                        =zip(*tdmarket_data.apply(self.strategy_calculate,args=(shift,) ,axis=1))




        return tdmarket_data

    def getstrategydataDF(self):

        tdmarket_data_json = self.options(symbol=self.symbol,
                                    # strategy="ANALYTICAL",
                                    strategy="SINGLE",
                                    contractType='ALL',
                                    includeQuotes=True)

        dfmerged=self.getstrategypreparedbasedataDF(tdmarket_data_json)

        return dfmerged











