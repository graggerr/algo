from api import StrategyRunnerAPI
from tests.conftest import prepare_conf


def test_zerroloss_strategy(tmp_path):
    test_configuration = prepare_conf(tmp_path)

    strategy_data=StrategyRunnerAPI.run_zerroloss_strategy(test_configuration,'SAVA')
    assert len(list(tmp_path.iterdir())) == 1 # one config.yaml and one keystore

    assert strategy_data.size >2

