'''
   Default test for Boilerplate App 
'''

from tobor.app import print_response, divide_balls


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
