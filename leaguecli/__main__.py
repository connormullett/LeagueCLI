#!/usr/bin/env python3

import click
import requests


def get_challengers():
    pass


def get_rank():
    pass


def summoner_lookup():
    pass


@click.command()
@click.argument('command')
@click.option('--verbose', '-v', help='Enable Verbosity', is_flag=True)
def main(command, verbose):
    if verbose:
        print(f'league {command}')
    if command == 'rank':
        click.echo('getting rank .. ')
