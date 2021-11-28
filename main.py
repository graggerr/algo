# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.
import api

strategyApi= api.StrategyRunnerAPI()

from Util import outputUtil

if __name__ == '__main__':
  symbol='SAVA'
  estimator = strategyApi.run_zerroloss_strategy(symbol)

  # onlu=y for feodor :)
  # options_data=tdclientOptionshelper().options(symbol=_symbol)
  # strategy_data =estimator.getstrategypreparedbasedataDF(options_data)
  strategy_data = estimator.getstrategydataDF()
  outputUtil.dataToExl(symbol, strategy_data)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
