#!/usr/bin/env python3

import click
import requests


BASE_URL = 'https://na1.api.riotgames.com/lol/'

def get_dev_key():
    with open('settings.txt', 'r') as f:
        return f.read().rstrip()


@click.group()
@click.option('--api', '-a', help='your riot games api key')
@click.option('--verbose', '-v', help='enable verbosity')
def main(api):
    api = get_dev_key() if api is None else api
    click.echo(api)


@main.command()
@click.option('--queue', '-q', help='queue type to search for', default='s')
@click.option('--limit', '-l', help='limit returned results starting from rank 1 ' \
        'to limit')
def challenger(queue):
    click.echo(queue)


@main.command()
def rank():
    pass


@main.command()
@click.argument('name', nargs=1)
def summoner(name):
    click.echo(name)


