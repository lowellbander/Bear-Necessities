import sys
sys.path.insert(0, '/simul8/env/bear/lib/python2.7/site-packages')
sys.path.insert(0, '/simul8/Bear-Necessities/api')

print sys.path

from run import make_app
application = make_app(settings='/simul8/Bear-Necessities/api/settings.py')

