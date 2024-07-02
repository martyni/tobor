'''
tobor twitch bot
'''
import random
from twitchio.ext import commands


from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open('/home/app/credentials') as creds_file:
   my_yaml = creds_file.read()

creds = load(my_yaml, Loader=Loader)


def print_response(ctx):
    print(ctx)
    print(type(ctx))
    return type(ctx)

def divide_balls(ball_number, ball_string='askmar1Lookballs '):
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
    return ball_list

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=creds['access_token'], prefix='?', initial_channels=['askmartyn'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        print_response(ctx)
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def dice(self, ctx: commands.Context):
        # Simulate a dice roll, a random number between 1 and 6
        await ctx.send(f'You rolled a {random.randint(1, 6)}')    
    
    @commands.command()
    async def balls(self, ctx: commands.Context):
        ball_number = random.randint(0, 69)
        ball_list = divide_balls(ball_number)
        for balls in ball_list:
            await ctx.send(f'{balls}') 

def main():
    bot = Bot()
    bot.run()
