
from click.testing import(
    CliRunner,
)


def call_CLI(fnc=None, parameters=None, envs=None):
    """
    Creates testing environment for cli application
    :param fnc: command to run
    :param parameters: program cmd argument
    :param envs:
    :return: invoked cli runner
    """
    fnc = fnc
    runner = CliRunner()
    envs = envs or {}
    parameters = parameters or []
    # catch exceptions enables debugger
    return runner.invoke(fnc, args=parameters, env=envs, catch_exceptions=True)