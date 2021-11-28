from pandas import DataFrame

from zerrolossstrategyestimator import zerroloss_strategy_TD_estimator


class strategyhandlerbase():
    pass

class zerroloss_strategy_handler(strategyhandlerbase):
    def __init__(self):
        pass


    # def handle(self,strategyDF)-> DataFrame :
    #     pass

    def handlestrategyDF(self,dfhandled):
        # zerrolossstrategyestimator = zerrolossstrategyestimator()

        # _symbol = 'SAVA'
        # filename = "output_zerrowloss_{}.xlsx".format(_symbol)

        # dataDF = requester.getstrategydata(symbol=_symbol.upper())
        # dfhandled =self.handle(dfhandled )

        dfhandled=dfhandled[(dfhandled['year_interest_of_strategy1'] > 100) &
                            (dfhandled['year_interest_of_strategy1'] < 50000) ]



        dfhandled = dfhandled.sort_values(by=['year_interest_of_strategy1']).head(10)


        return dfhandled