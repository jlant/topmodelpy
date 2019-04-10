"""Main `topmodelpy` command line interface"""


import click
import sys


class Options:
    def __init__(self):
        self.verbose = False
        self.show = False


# Create a decorator to pass options to each command
pass_options = click.make_pass_decorator(Options, ensure=True)


@click.group()
@click.option("-v", "--verbose", is_flag=True,
              help="Print model run details.")
@click.option("-s", "--show", is_flag=True,
              help="Show output plots.")
@click.pass_context
def main(options, verbose, show):
    """Topmodelpy is a command line tool for a rainfall-runoff
    model that predicts the amount of water flow in rivers.

    Specificiations for a model run are contained in a configuration file.
    """
    options.verbose = verbose
    options.show = show


@main.command()
@click.argument("configfile", type=click.Path(exists=True))
@pass_options
def run(options, configfile):
    try:
        click.echo("Run configfile")
        click.echo(configfile)
    except Exception as err:
        click.echo(err)
        sys.exit(1)

    if options.verbose:
        click.echo("Verbose on")
    if options.show:
        click.echo("Show on")


@main.command()
@pass_options
def runexample(options):
    try:
        click.echo("Run example")
    except Exception as err:
        click.echo(err)

    if options.verbose:
        click.echo("Verbose on")
    if options.show:
        click.echo("Show on")
