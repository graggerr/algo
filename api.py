from strategies.estimators.zerrolossstrategyestimator import StrategyEstimatorZerroloss_TD
from strategies.handlers.zerrolosstrategyhandler import StrategyHandlerZerroloss


class StrategyRunnerAPI:

    @staticmethod
    def run_zerroloss_strategy(configuration,simbol):
        estimator = StrategyEstimatorZerroloss_TD(simbol)
        # onlu=y for feodor :)
        # options_data=tdclientOptionshelper().options(symbol=_symbol)
        # strategy_data =estimator.getstrategypreparedbasedataDF(options_data)
        strategy_data = estimator.getStrategyData()
        # outputUtil.dataToExl(_symbol, strategy_data)


        #print output

        return strategy_data

    @staticmethod
    def handle_zerroloss_strategy(configuration,strategy_data_df):
        # return best operations
        handler =StrategyHandlerZerroloss()
        return handler.handleStrategy(strategy_data_df)


