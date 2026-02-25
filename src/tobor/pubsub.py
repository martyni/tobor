import twitchio
from twitchio import eventsub
import requests
from random import choice
from tobor.auth import creds, TWITCH_INTEGRATION, LINKS


access_token = creds['TOBOR_ACCESS_TOKEN']
refresh_token = creds['TOBOR_REFRESH_TOKEN']
my_channel_id = creds['MY_CHANNEL_ID']


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


class BitsClient(twitchio.Client):

    async def load_tokens(self, path=None):
        await self.add_token(access_token, refresh_token)

    async def setup_hook(self):
        print(f'connecting to channel: {my_channel_id}')
        payload = eventsub.ChannelBitsUseSubscription(broadcaster_user_id=my_channel_id)
        await self.subscribe_websocket(payload=payload)

    async def event_channel_bits_use(self, event: twitchio.ChannelBitsUse):
        print('bits message')
        print(event.text)
        message = f'{event.user.name} sent {event.bits} {random_bit_word()}!'
        if event.text:
            message += f' {event.text}'
        message_ticker(message)


client = BitsClient(
    client_id=creds['TOBOR_CLIENT_ID'],
    client_secret=creds['TOBOR_CLIENT_SECRET'])


def main():
    client.run()


if __name__ == "__main__":
    main()
