'''
tobor twitch bot
'''
import random
from twitchio.ext import commands
import os
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

TWITCH_INTEGRATION = 'https://support.discord.com/hc/en-us/articles/212112068-Twitch-Integration-FAQ#h_01GBQS1H1GHA13S6S3NX3114QC'  
LINKS = 'https://linktr.ee/askmartyn'

if os.environ.get('TOBOR_ACCESS_TOKEN') is not None:
    print('loading env vars')

    creds = {
            'access_token': os.environ.get('TOBOR_ACCESS_TOKEN'),
             'refresh_token': os.environ.get('TOBOR_REFRESH_TOKEN'),
             'client_id': os.environ.get('TOBOR_CLIENT_ID')
             }
else:    
    print('loading credentials from file')

    with open('/home/app/credentials') as creds_file:
        my_yaml = creds_file.read()
    creds = load(my_yaml, Loader=Loader)


def print_response(ctx):
    print(ctx)
    print(type(ctx))
    return type(ctx)

def divide_balls(ball_number, ball_string='askmar1Lookballs ', objects='balls'):
    ball_list = []
    combined_ball_string = f'{ ball_string * ball_number}'
    ball_limit = 500 // len(ball_string)
    if ball_number >= ball_limit:
        print(f'{ball_number} is more than {ball_limit}')
        ball_list.append(f'{ball_string * ball_limit}')
        if ball_number / ball_limit > 2:
            print(f'{ball_number} is more than {ball_limit * 2}')
            ball_list.append(f'{ball_string * ball_limit}')
        remaining_balls = ball_number % ball_limit    
        print(f'{remaining_balls} is the remaining balls')
        ball_list.append(f'{ball_string * remaining_balls}')         
    else:
        ball_list.append(combined_ball_string)
    ball_list.append(f'{ball_number} {objects}')    
    return ball_list

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        self.__exclusions = [i for i in dir(self)]
        super().__init__(token=creds['access_token'], prefix='*', initial_channels=['askmartyn'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}') 
    

    @commands.command()
    async def balls(self, ctx: commands.Context):
        ball_number = random.randint(0, 69)
        ball_list = divide_balls(ball_number)
        for balls in ball_list:
            await ctx.send(f'{balls}')    
            
    @commands.command()
    async def content_warning(self, ctx: commands.Context):
        warnings = [
        '''FLASHING IMAGES AND BRIGHT COLOURS people with photosensitivity or who have sensory overload may need to look elsewhere. You have been warned''',
        '''The askMartyn channel is a LGBTQ+, sex positive stream for people who don't mind rude words, innuendo, bad behavior and general naughtiness. As such you may read or hear something that you find offensive. We will not tolerate hate speech, racism, transphobia or people being dicks (you know who you are) zero tolerance.You have been warned'''
        ]
        for warning in warnings:
            await ctx.send(f'{warning}')

    @commands.command()
    async def roll_dice(self, ctx: commands.Context):
        # Simulate a dice roll, a random number between 1 and 6
        await ctx.send(f'You rolled a {random.randint(1, 6)}')    

    @commands.command()
    async def coinflip(self, ctx: commands.Context):
        # Flip a coin!
        await ctx.send(random.choice(['Heads!', 'Tails!']))

    @commands.command()
    async def discord(self, ctx: commands.Context):
        return await ctx.send(f'{TWITCH_INTEGRATION}')
    
    @commands.command()
    async def eelee(self, ctx: commands.Context):
        ball_number = random.randint(0, 69)
        ball_list = divide_balls(ball_number, ball_string='askmar1Eelee ', objects='eelees')
        for balls in ball_list:
            await ctx.send(f'{balls}')    
    
    @commands.command()
    async def fluid(self, ctx: commands.Context):
        fluid_choice = random.choice(['wet', 'moisten', 'fluid', 'slorp', 'wazz', 'spit', 'squirt' ])
        await ctx.send(f'{fluid_choice} yourself')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        print_response(ctx)
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def nerd(self, ctx: commands.Context):
        your_choices = random.choice(['you','yew', 'your', 'ur', 'you\'re', 'you are', 'u are', 'thou art' ])
        nerd_choices = random.choice(['nerd','newt', 'nord', 'nearrrrd','NERD!!', 'nooooooord', 'naaaard'])
        await ctx.send(f'{your_choices} a {nerd_choices}')
    
    @commands.command()
    async def _(self, ctx: commands.Context):
        await ctx.send('...coming soon...')


def main():
    bot = Bot()
    bot.run()
