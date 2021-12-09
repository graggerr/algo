# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.
from  MarketScanner import MarketScanner
from configuration import Configuration
from strategies.estimators.zerrolossstrategyestimator import StrategyEstimatorZerroloss_TD
from strategies.handlers.zerrolosstrategyhandler import StrategyHandlerZerroloss

#strategyApi= api.StrategyRunnerAPI()
#configuration = Configuration().load_configuration()

from Util import outputUtil

if __name__ == '__main__':
 
  scanner = MarketScanner()
  symbol=scanner.getSymbols()
  estimator = StrategyEstimatorZerroloss_TD(symbol[0])
  handler =StrategyHandlerZerroloss()

  strategy_data = estimator.getStrategyData()
  operation_data = handler.handleStrategy(strategy_data)


  print(strategy_data)


  outputUtil.dataToExl(symbol[0],'zerroloss', strategy_data)
  print(operation_data)
  outputUtil.dataToExl(symbol[0],'zerroloss_handler', operation_data)
#test
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
