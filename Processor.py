
from Util import outputUtil
from config import td_consumer_key
from tddataprovider import tdclientOptionshelper
from zerrolossstrategyestimator import zerroloss_strategy_TD_estimator
from zerrolosstrategyhandler import zerroloss_strategy_handler


def proccess():
    # requester = zerrolossstrategubuilder()
    print('Start')
    _symbol = 'SAVA'
    estimator = zerroloss_strategy_TD_estimator(_symbol)
    # onlu=y for feodor :)
    # options_data=tdclientOptionshelper().options(symbol=_symbol)
    # strategy_data =estimator.getstrategypreparedbasedataDF(options_data)
    strategy_data = estimator.getstrategydataDF()
    outputUtil.dataToExl(_symbol, strategy_data)
    print('Stop')


if __name__ == '__main__':
    proccess()


