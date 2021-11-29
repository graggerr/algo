import api
from configuration import Configuration

strategyApi= api.StrategyRunnerAPI()
configuration = Configuration().load_configuration()

def proccess(symbol ):

    print('Start')
    strategy_data =strategyApi.run_zerroloss_strategy(configuration,symbol)

    print('Stop')


if __name__ == '__main__':
    proccess('SAVA')


