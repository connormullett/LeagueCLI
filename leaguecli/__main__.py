#!/usr/bin/env python3

import click
import requests


def get_dev_key():
    with open('settings.txt', 'r') as f:
        return f.read().rstrip()


@click.group()
@click.option('--api', '-a', help='your riot games api key')
def main(api):
    pass


@main.command()
def challenger():
    pass


@main.command()
def rank():
    pass


@main.command()
def summoner():
    pass


