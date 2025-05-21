import os
import twitchio
from twitchio.ext import pubsub
import requests
from random import choice

if os.environ.get('TOBOR_ACCESS_TOKEN') is not None:
    print('loading env vars')

    creds = {
            'access_token': os.environ.get('TOBOR_ACCESS_TOKEN'),
             'refresh_token': os.environ.get('TOBOR_REFRESH_TOKEN'),
             'client_id': os.environ.get('TOBOR_CLIENT_ID'),
             'user_token': os.environ.get('TOBOR_USER_TOKEN'),
             'mod_user_channel_id': int(os.environ.get('MOD_USER_CHANNEL_ID')),
             'my_channel_id': int(os.environ.get('MY_CHANNEL_ID')),            
             }
else:    
    print('loading credentials from file')

    with open('/home/app/credentials') as creds_file:
        my_yaml = creds_file.read()
    creds = load(my_yaml, Loader=Loader)


access_token = creds['access_token']
user_token = creds['user_token']
my_channel_id = creds['my_channel_id']
mod_user_channel_id = creds['mod_user_channel_id']
client = twitchio.Client(token=access_token)
client.pubsub = pubsub.PubSubPool(client)
def strip_phrase(phrase, message):
    print(f'removing {phrase} from {message}')
    return message.replace(phrase,'')

def random_bit_word():
    return choice(['bits','bittys','borts','8008135'])

def message_ticker(message, ticker_host='http://ticker'):
    ticker_url=f'{ticker_host}/message/{message}'
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
