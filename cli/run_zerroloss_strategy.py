import click

from cli.utils_cli import get_api


def zl_strategy_print(data):
    return data


@click.command()
@click.option('-s', '--simbol', default=None, prompt='sombol to run',
              help='please add simbol to run.')
def run_zerroloss_strategy( symbol):
    """runm zerro loss strategy."""

    api = get_api()

    try:
        data =api.run_zerroloss_strategy( symbol)
        click.echo(zl_strategy_print(data))
    except :
        click.echo('Invalid parameters or something goin bad!')




