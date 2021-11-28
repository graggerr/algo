import api
from Util import outputUtil

proccessorApi= api.StrategyRunnerAPI()

def proccess(symbol ):

    print('Start')
    estimator =proccessorApi.run_zerroloss_strategy(symbol)


    # onlu=y for feodor :)
    # options_data=tdclientOptionshelper().options(symbol=_symbol)
    # strategy_data =estimator.getstrategypreparedbasedataDF(options_data)
    strategy_data = estimator.getstrategydataDF()
    outputUtil.dataToExl(symbol, strategy_data)
    print('Stop')


if __name__ == '__main__':
    proccess()


