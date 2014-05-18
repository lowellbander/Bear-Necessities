import os

from eve import Eve

def make_app(*args, **kwargs):
    '''
    Factory for making an Eve application.
    This is needed to ensure that wsgi.py and run.py have the same methods for
    instantiating the Eve application
    '''
    return Eve(*args, **kwargs)

if __name__ == '__main__':
    make_app().run(host='0.0.0.0')
