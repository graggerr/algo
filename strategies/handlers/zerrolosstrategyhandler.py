class strategyhandlerbase():
    pass

class zerroloss_strategy_handler(strategyhandlerbase):
    def __init__(self):
        pass


    # def handle(self,strategyDF)-> DataFrame :
    #     pass

    def handlestrategyDF(self,strategy_data_df):
        # zerrolossstrategyestimator = zerrolossstrategyestimator()

        # _symbol = 'SAVA'
        # filename = "output_zerrowloss_{}.xlsx".format(_symbol)

        # dataDF = requester.getstrategydata(symbol=_symbol.upper())
        # dfhandled =self.handle(dfhandled )

        strategy_data_df=strategy_data_df[(strategy_data_df['year_interest_of_strategy1'] > 60) &
                            (strategy_data_df['year_interest_of_strategy1'] < 50000) ]



        strategy_data_df = strategy_data_df.sort_values(by=['year_interest_of_strategy1']).head(10)


        return strategy_data_df