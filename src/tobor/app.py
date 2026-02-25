'''
tobor twitch bot
'''
import random
import pydoc
import inspect
from twitchio.ext import commands
import os
from yaml import load
from tobor.home_ass import HomeAss
from tobor.colours import colours
from tobor.auth import creds,TWITCH_INTEGRATION, LINKS
import requests as req


def print_response(ctx):
    print(ctx)
    print(type(ctx))
    return type(ctx)


def divide_balls(
        ball_number,
        ball_string='askmar1Lookballs ',
        objects='balls'):
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

def log_events(message, user, data_url="https://twitch.tv/askmartyn", platform="twitch", url="https://eventlogger.askmartyn.com:6969/event"):
    data={
            "message": message,
            "user": user,
            "url": data_url,
            "platform": platform
            }
    print(f"{url}, data: {data}")
    req.post(  json=data, url=url )

    



class notBot(commands.Bot):
    def __init__(self):
        super()
            

class Bot(commands.Bot):
    helpful_dict = {
            'balls': 'Balls everywhere',
            'cw': 'Content Warnings',
            'dice':'Simulate a dice roll, a random number between 1 and 6',
            'd20':'Simulate a d20 roll, a random number between 1 and 20',
            'flipcoin': 'Flip a coin!',
            'coinflip': 'Flip a coin!',
            'rgbcolour': 'Mysterious rgbcolour function, nothing to see here. Not suss',
            'colour': 'Mysterious colour function, nothing to see here. Not suss',
            'colours': 'Mysterious colours function, nothing to see here. Not suss',
            'discord': 'Show discord instructions',
            'hello': 'Say hello',
            'help': 'Help function, show all commands, or check help for other commands',
            'eelee': 'Show love with eelee',
            'fluid': 'Get askMartyn to drink'
            }

    def __init__(self, creds=creds):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of
        # strings...
        self.creds=creds
        self.__exclusions = [i for i in dir(self)]
        self.colours_list = colours
        self.unwanted_methods = set(dir(notBot()))
        self.ha = HomeAss(self.creds['BALLS_HOST'],self.creds['BALLS_FILE'])
        super().__init__(
            token=self.creds['TOBOR_ACCESS_TOKEN'],
            prefix='!',
            initial_channels=['askmartyn'])

    def get_method_attr(self, attr):
        return getattr(self, attr)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def balls(self, ctx: commands.Context):
        self.helpful_dict['balls']
        ball_number = random.randint(0, 69)
        self.ha.put_balls(ball_number)
        ball_list = divide_balls(ball_number)
        for balls in ball_list:
            await ctx.send(f'{balls}')
        if ball_number == 69:
            log_events("Congratulate the Ball Master!", f"{ctx.author.name}")
            await ctx.send(f'nice work {ctx.author.name}')

    @commands.command()
    async def cw(self, ctx: commands.Context):
        self.helpful_dict['cw']
        warnings = [
            '''FLASHING IMAGES AND BRIGHT COLOURS people with photosensitivity or who have sensory overload may need to look elsewhere. You have been warned''',
            '''The askMartyn channel is a LGBTQ+, sex positive stream for people who don't mind rude words, innuendo, bad behavior and general naughtiness. As such you may read or hear something that you find offensive. We will not tolerate hate speech, racism, transphobia or people being dicks (you know who you are) zero tolerance.You have been warned''']
        for warning in warnings:
            await ctx.send(f'{warning}')

    @commands.command()
    async def dice(self, ctx: commands.Context):
        self.helpful_dict['dice']
        roll = random.randint(1, 6)
        self.ha.put_keys(dice=roll)
        await ctx.send(f'You rolled a {roll}')

    @commands.command()
    async def d20(self, ctx: commands.Context):
        self.helpful_dict['d20']
        
        roll = random.randint(1, 20)
        self.ha.put_keys(d20=roll)
        if roll == 20:
           await ctx.send(f'{ctx.author.name} ROLLED A NAT {roll}!!!!')
        else:
           await ctx.send(f'{ctx.author.name} rolled a {roll}')

    @commands.command()
    async def coinflip(self, ctx: commands.Context):
        self.helpful_dict['flipcoin']
        coin = random.choice(['Heads', 'Tails'])
        self.ha.put_keys(coin=coin)
        await ctx.send(f'{coin}!')

    @commands.command()
    async def flipcoin(self, ctx: commands.Context):
        self.helpful_dict['flipcoin']
        coin = random.choice(['Heads', 'Tails'])
        self.ha.put_keys(coin=coin)
        await ctx.send(f'{coin}!')

    @commands.command()
    async def rgbcolour(self, ctx: commands.Context, red: int, green: int, blue: int):
        self.helpful_dict['rgbcolour']
        print(red)
        print(green)
        print(blue)
        colour_obj={
                "red": abs(red),
                "green": abs(green),
                "blue": abs(blue),
                }
        for col in colour_obj:
            colour_obj[col] = colour_obj[col] if colour_obj[col] <= 255 else 255
        self.ha.put_keys(colour=colour_obj)
        await ctx.send(f'Setting light to r: {colour_obj["red"]} g: {colour_obj["green"]} b: {colour_obj["blue"]} (give it a minute)')

    @commands.command()
    async def colour(self, ctx: commands.Context, *args):
        self.helpful_dict['colour']
        raw_colour = " ".join([ _.lower() for _ in args])
        lookup_colour = raw_colour.lower().replace(" ","")
        if lookup_colour in  self.colours_list:
          self.ha.put_keys(raw_colour=lookup_colour)
          log_events(lookup_colour, f"{ctx.author.name}")
          await ctx.send(f'Setting light to {raw_colour}')
        else: 
          creative_colour = self.colours_list.pop()
          remaining_colours = len(self.colours_list)
          self.ha.put_keys(raw_colour=lookup_colour)
          log_events(lookup_colour, f"{ctx.author.name}")
          await ctx.send(f'{raw_colour} is not a creative colour, setting to {creative_colour}. {remaining_colours} colours remaining.')


    @commands.command()
    async def discord(self, ctx: commands.Context):
        self.helpful_dict['discord']
        return await ctx.send(f'{TWITCH_INTEGRATION}')

    @commands.command()
    async def eelee(self, ctx: commands.Context):
        self.helpful_dict['eelee']
        ball_number = random.randint(0, 69)
        self.ha.put_balls(ball_number, "eelee")
        ball_list = divide_balls(
            ball_number,
            ball_string='askmar1Eelee ',
            objects='eelees')
        for balls in ball_list:
            await ctx.send(f'{balls}')
        if ball_number == 69:
            log_events("They really care", f"{ctx.author.name}")
            await ctx.send('aw, thats nice')

    @commands.command()
    async def fluid(self, ctx: commands.Context):
        self.helpful_dict['fluid']
        fluid_choice = random.choice(
            ['wet', 'moisten', 'fluid', 'slorp', 'wazz', 'drool', 'squirt'])
        log_events(f"{fluid_choice} yourself", f"{ctx.author.name}")
        await ctx.send(f'{fluid_choice} yourself')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        self.helpful_dict['hello']
        print_response(ctx)
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def nerd(self, ctx: commands.Context):
        self.helpful_dict['nerd']
        '''Call someone a nerd, randomly'''
        your_choices = random.choice(
            ['you', 'yew', 'your', 'ur', 'you\'re', 'you are', 'u are', 'thou art'])
        nerd_choices = random.choice(
            ['nerd', 'newt', 'nord', 'nearrrrd', 'NERD!!', 'nooooooord', 'naaaard'])
        await ctx.send(f'{ctx.author.name} thinks {your_choices} a {nerd_choices}')

    @commands.command()
    async def help(self, ctx: commands.Context, *args):
        self.helpful_dict['help']
        list_of_commands = ""
        if len(args) < 1:
           for item in dir(self):
               if '_' not in item and item not in self.unwanted_methods: 
                  list_of_commands += f'!{item}, '
           await ctx.send(list_of_commands)
        else: 
          for arg in args:
             help_string = self.helpful_dict.get(arg)
             if help_string:
                await ctx.send(f'{arg}: {help_string}')
             else:
                await ctx.send(f'{arg} is not a valid command')



    @commands.command()
    async def _(self, ctx: commands.Context):
        await ctx.send('...coming soon...')



def main():
    bot = Bot()
    bot.run()

