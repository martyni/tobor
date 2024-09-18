
import twitchio
from twitchio.ext import pubsub
import requests

if os.environ.get('TOBOR_ACCESS_TOKEN') is not None:
    print('loading env vars')

    creds = {
            'access_token': os.environ.get('TOBOR_ACCESS_TOKEN'),
             'refresh_token': os.environ.get('TOBOR_REFRESH_TOKEN'),
             'client_id': os.environ.get('TOBOR_CLIENT_ID'),
             'user_token': os.environ.get('TOBOR_USER_TOKEN'),
             'mod_user_channel_id': os.environ.get('MOD_USER_CHANNEL_ID'),
             'my_channel_id': os.environ.get('TOBOR_MY_CHANNEL_ID'),            
             }
else:    
    print('loading credentials from file')

    with open('/home/app/credentials') as creds_file:
        my_yaml = creds_file.read()
    creds = load(my_yaml, Loader=Loader)


my_token = creds['access_token']
users_oauth_token = creds['user_token']
users_channel_id = creds['my_channel_id']
mods_channel_id = creds['mod_user_channel_id']
client = twitchio.Client(token=my_token)
client.pubsub = pubsub.PubSubPool(client)


@client.event()
async def event_pubsub_bits(event: pubsub.PubSubBitsMessage):
    print('bits message')
    print(event.message.content)  
    requests.get(f"http://ticker/message/${event.message.content}") 
    print(event.bits_used)
    print(event.user) 

@client.event()
async def event_pubsub_channel(event: pubsub.PubSubChannelPointsMessage):
    print('chat message')
    print(event)   

@client.event()
async def event_pubsub_chat(event: pubsub.PubSubChatMessage): 
    print('subscription message')
    print(event)

async def main():
    topics = [
        pubsub.bits(users_oauth_token)[users_channel_id],
        pubsub.channel_points(users_oauth_token)[users_channel_id],
    ]
    await client.pubsub.subscribe_topics(topics)
    await client.start()

client.loop.run_until_complete(main())
