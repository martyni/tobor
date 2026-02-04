'''
   Default test for Boilerplate App
'''

from tobor.auth import creds,TWITCH_INTEGRATION, LINKS
from tobor.app import print_response, divide_balls, Bot

print(creds)
def test_print_response():
    '''
    Test of main function for default app
    '''

    assert print_response("balls") is str, f'incorrect type returned'


def test_divide_balls():
    '''
    Test of main function for default app
    '''
    assert divide_balls(1) == ['askmar1Lookballs ', '1 balls']
    assert len(divide_balls(30)) is 3
    assert len(divide_balls(60)) is 4

def test_bot(creds=creds):
    '''
    Test bot loads
    '''
    creds['BALLS_HOST'] = 'localhost'
    creds['BALLS_FILE'] = 'file'
    bot = Bot(creds=creds)
