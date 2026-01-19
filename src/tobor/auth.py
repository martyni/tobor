'''
tobor twitch bot
'''
import random
from twitchio.ext import commands
import os
from yaml import load
from tobor.home_ass import HomeAss
import sys

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

TWITCH_INTEGRATION = 'https://support.discord.com/hc/en-us/articles/212112068-Twitch-Integration-FAQ#h_01GBQS1H1GHA13S6S3NX3114QC'
LINKS = 'https://linktr.ee/askmartyn'
print(sys.argv)
print(len(sys.argv))

if len(sys.argv) > 1:
    CREDS=sys.argv[1]
else:
    CREDS='/home/app/credentials'

if os.environ.get('TOBOR_ACCESS_TOKEN') is not None:
    print('loading env vars')

    creds = {
        'TOBOR_ACCESS_TOKEN': os.environ.get('TOBOR_ACCESS_TOKEN'),
        'TOBOR_REFRESH_TOKEN': os.environ.get('TOBOR_REFRESH_TOKEN'),
        'TOBOR_CLIENT_ID': os.environ.get('TOBOR_CLIENT_ID'),
        'TOBOR_USER_TOKEN': os.environ.get('TOBOR_USER_TOKEN'),
        'MOD_USER_CHANNEL_ID': os.environ.get('MOD_USER_CHANNEL_ID'),
        'MY_CHANNEL_ID': os.environ.get('MY_CHANNEL_ID'),
        'BALLS_FILE': os.environ.get('BALLS_FILE'),
        'BALLS_HOST': os.environ.get('BALLS_HOST'),
    }
else:
    print('loading credentials from file')

    with open(CREDS) as creds_file:
        my_yaml = creds_file.read()
    creds = load(my_yaml, Loader=Loader)
