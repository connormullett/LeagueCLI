#!/usr/bin/env python3

import click
import requests
import operator


BASE_URL = 'https://na1.api.riotgames.com/lol/'

def get_dev_key():
    with open('settings.txt', 'r') as f:
        return f.read().rstrip()


@click.group()
@click.option('--api', '-a', help='your riot games api key')
@click.option('--verbose', '-v', help='enable verbosity', is_flag=True)
@click.pass_context
def main(ctx, api, verbose):
    ctx.obj = {}
    if not api:
        api = get_dev_key()
    ctx.obj['api'] = api
    ctx.obj['api'] = api
    ctx.obj['verbose'] = verbose


@main.command()
@click.option('--queue', '-q', help='queue type to search for. s = solo, f = flex, t = treeline', default='s')
@click.option('--limit', '-l', help='limit returned results starting from rank 1 ' \
        'to limit')
@click.pass_context
def challenger(ctx, queue, limit):
    queue_mapper = {
                's': 'RANKED_SOLO_5x5',
                'f': 'RANKED_FLEX_SR',
                't': 'RANKED_FLEX_TT'
            }

    queue = queue_mapper[queue]

    if ctx.obj['verbose']:
        click.echo('using api key %s' % (ctx.obj['api']))
        click.echo(f'Searching challenger queue {queue}')

    response = requests.get(f"{BASE_URL}league/v4/challengerleagues/by-queue/{queue}?api_key={ctx.obj['api']}")

    if ctx.obj['verbose']:
        click.echo('response status %s' % (response.status_code))

    ladder = response.json()['entries']
    players = sorted(ladder, key=lambda entry: entry['leaguePoints'], reverse=True)

    click.secho('%16s %16s' % ('NAME', 'POINTS'), fg='blue', bold=True)
    if not limit:
        for player in players:
            click.echo('%16s %16s' % (player['summonerName'], player['leaguePoints']))
    else:
        for i, player in enumerate(players):
            click.echo('%16s %16s' % (player['summonerName'], player['leaguePoints']))
            if i + 1 >= int(limit):
                break


@main.command()
def rank():
    pass


@main.command()
@click.argument('name', nargs=1)
def summoner(name):
    click.echo(name)

