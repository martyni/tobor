'''
   Default test for Boilerplate App
'''

from  tobor.home_ass import HomeAss 

from random import randint
HA = HomeAss('localhost', 'file')


def random_string(length=6):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    rand_str = ""
    for c in range(length): 
       rand_str += alphabet[randint(0, len(alphabet) - 1)]
    return rand_str

def test_create_db():
    '''
    Test of main function for default app
    '''
    test_object = {random_string(): random_string()}

    HA.reset_object()
    assert HA.ball_object == {}
    HA.put_keys(**test_object)
    HA.get_object()
    assert HA.ball_object == test_object


def test_balls():
    '''
    Test of main function for default app
    '''
    first_balls =  randint(0, 69)
    HA.reset_object({})
    HA.put_keys(balls=0)
    HA.put_balls(first_balls)
    assert HA.ball_object == {"balls": first_balls}
    scnd_balls =  randint(0, 69)
    HA.put_balls(scnd_balls)
    HA.get_object()
    assert HA.ball_object == {"balls": first_balls + scnd_balls}
