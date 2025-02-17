import click
from typing import Optional

@click.group()
def cli():
    """Changelog LLM - Find changelogs between library versions"""
    pass

@cli.command()
@click.argument('package_name')
@click.argument('from_version')
@click.argument('to_version')
def compare(package_name: str, from_version: str, to_version: str):
    """Compare changelogs between two versions of a package"""
    click.echo(f"Finding changelog for {package_name} from {from_version} to {to_version}")
    # TODO: Implement actual changelog retrieval logic
    click.echo("Changelog retrieval not yet implemented")

if __name__ == '__main__':
    cli()