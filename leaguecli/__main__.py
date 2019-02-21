#!/usr/bin/env python3

import click
import requests


def get_challengers():
    pass


def get_rank():
    pass


def get_summoner():
    pass


@click.command()
@click.argument('command')
@click.option('--verbose', '-v', help='Enable Verbosity', is_flag=True)
@click.option('--api', '-a', help='Your Riot Games API Key')
def main(command, api, verbose):

    command_mapper = {
        'challengers': get_challengers,
        'rank': get_rank,
        'summoner': get_summoner
    }

    if verbose:
        click.echo(click.style(f'league {command}', fg='bright_blue'))
        if api:
            click.echo(click.style(f'using api key {api}', fg='bright_blue'))

    if callable(command_mapper[command]):
        r = command_mapper[command]
        r()
