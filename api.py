from strategies.zerrolossstrategyestimator import zerroloss_strategy_TD_estimator
from strategies.zerrolosstrategyhandler import zerroloss_strategy_handler


class StrategyRunnerAPI:

    @staticmethod
    def run_zerroloss_strategy(simbol):
        estimator = zerroloss_strategy_TD_estimator(simbol)
        # onlu=y for feodor :)
        # options_data=tdclientOptionshelper().options(symbol=_symbol)
        # strategy_data =estimator.getstrategypreparedbasedataDF(options_data)
        strategy_data = estimator.getstrategydataDF()
        # outputUtil.dataToExl(_symbol, strategy_data)
        # print('Stop')

        #print output

        return strategy_data

    @staticmethod
    def handle_zerroloss_strategy(strategy_data_df):
        # return best operations
        handler =zerroloss_strategy_handler()
        return handler.handlestrategyDF(strategy_data_df)


