import click

from cli.run_zerroloss_strategy import (
    run_zerroloss_strategy,
)

@click.group()
def strategies_cli():
    pass


strategies_cli.add_command(run_zerroloss_strategy)


if __name__ == "__main__":
    strategies_cli()


