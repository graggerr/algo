# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.
import api
from configuration import Configuration

strategyApi= api.StrategyRunnerAPI()
configuration = Configuration().load_configuration()

from Util import outputUtil

if __name__ == '__main__':
  symbol='SAVA'
  strategy_data =strategyApi.run_zerroloss_strategy(configuration,symbol)
  outputUtil.dataToExl(symbol,strategy_data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
