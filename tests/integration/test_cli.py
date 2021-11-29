import pytest

from cli.strategies_cli import strategies_cli
from tests.cli_tester import (
     call_CLI,
)


def test_base_help():

    result = call_CLI(strategies_cli,parameters=["--help"])
    assert result.exit_code == 0
    assert "Usage: strategies-cli [OPTIONS] COMMAND [ARGS]" in result.output



@pytest.mark.parametrize(
    "subcommand", ["run-zerroloss-strategy"]
)


def test_base_subcommand_help(subcommand):
    result = call_CLI(strategies_cli, parameters=[subcommand, "--help"])
    assert result.exit_code == 0
    assert f"Usage: strategies-cli {subcommand} [OPTIONS]" in result.output



# !!! be careful this test will override keystore file on specific path
# def test_new_account(mocker, tmp_path):
#     conftest.prepare_conf(tmp_path)
#
#     mocker.patch('getpass.getpass',
#                  return_value='my-password')
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         result = runner.invoke(new_wallet)
#         assert result.exit_code == 0
#
#         result = runner.invoke(get_wallet)
#         assert result.exit_code == 0
#
#         result = runner.invoke(reveal_private_key)
#         assert result.exit_code == 0
