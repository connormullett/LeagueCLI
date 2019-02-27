#!/usr/bin/env python3

import click
import requests
import operator
import tzlocal

from datetime import datetime


TIMEZONE = tzlocal.get_localzone()
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


@main.command(help='display ranked stats by summoner name and other useful information')
@click.argument('name')
@click.pass_context
def rank(ctx, name):
    api = ctx.obj['api']
    verbose = ctx.obj['verbose']

    if verbose:
        click.echo(f'using api key {api}')
        click.echo(f'grabbing summoner {name}')

    name = name.replace(' ', '%20')
    response = requests.get(f'{BASE_URL}summoner/v4/summoners/by-name/{name}?api_key={api}')

    if verbose:
        click.echo(f'Status: {response.status_code}')

    try:
        summ_id = response.json()['id']
        player_data = requests.get(f'{BASE_URL}league/v4/positions/by-summoner/{summ_id}?api_key={api}')
        player_data = player_data.json()[0]
        click.echo(f"{player_data['tier']}  {player_data['rank']}")
    except KeyError:
        click.secho('No player data found', fg='red', bold=True)


@main.command(help='search summoners, wrap multiword names in \'\'')
@click.argument('name')
@click.option('--games', '-g', help='how many games to display')
@click.pass_context
def summoner(ctx, name, games):
    '''
    looks up by summoner name and shows past 20 games,
    rank, and top 3 champs with highest mastery
    '''

    def get_champ_mastery(summ_id):
        '''
        returns json serializable string containing
        top 3 champs with highest mastery
        '''
        response = requests.get(f'{BASE_URL}champion-mastery/v4/champion-masteries/by-summoner/{summ_id}?api_key={api}')
        return response.json()[:3]

    api = ctx.obj['api']
    verbose = ctx.obj['verbose']

    if verbose:
        pass

    click.echo(name.capitalize())
    name = name.replace(' ', '%20')

    response = requests.get(f'{BASE_URL}summoner/v4/summoners/by-name/{name}?api_key={api}')

    summ_id = response.json()['id']
    top_3_champs = get_champ_mastery(summ_id)

    for champ in top_3_champs:
        click.echo(f"{champ['championId']}\t{champ['championLevel']}")

