'''
   Default test for Boilerplate App
'''

from tobor.colours import colours

def test_colours():
    '''
    Test colours set works
    '''

    assert type(colours) is set, f'incorrect type returned'
    assert "red" in colours , f'red is not there. Boo!'


