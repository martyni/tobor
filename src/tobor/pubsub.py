import os
import twitchio
from twitchio.ext import pubsub
import requests
from random import choice
from yaml import load
from tobor.auth import creds,TWITCH_INTEGRATION, LINKS


access_token = creds['TOBOR_ACCESS_TOKEN']
user_token = creds['TOBOR_USER_TOKEN']
my_channel_id = creds['MY_CHANNEL_ID']
mod_user_channel_id = creds['MOD_USER_CHANNEL_ID']
client = twitchio.Client(token=access_token)
client.pubsub = pubsub.PubSubPool(client)


def strip_phrase(phrase, message):
    print(f'removing {phrase} from {message}')
    return message.replace(phrase, '')


def random_bit_word():
    return choice(['bits', 'bittys', 'borts', '8008135'])


def message_ticker(message, ticker_host='http://ticker'):
    ticker_url = f'{ticker_host}/message/{message}'
    print(f'sending ${ticker_url}')
    requests.get(ticker_url)
    print('sent')


@client.event()
async def event_pubsub_bits(event: pubsub.PubSubBitsMessage):
    print('bits message')
    print(event.message.content)
    message = strip_phrase(f'Cheer{event.bits_used}', event.message.content)
    message = f'{event.user.name} sent {event.bits_used} {random_bit_word()}! {message}'
    message_ticker(message)


async def loop():
    print(f'connecting to channel: {my_channel_id}')
    topics = [
        pubsub.bits(user_token)[my_channel_id],
    ]
    await client.pubsub.subscribe_topics(topics)
    await client.start()


def main():
    client.loop.run_until_complete(loop())


if __name__ == "__main__":
    main()
