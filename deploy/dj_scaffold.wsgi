import os
import site
from dj_scaffold.env import add_site_dir

HERE = os.path.dirname(__file__)
ROOT_PATH = os.path.abspath(os.path.join(HERE, '../'))

ALLDIRS = [os.path.join(ROOT_PATH, 'env/lib/python2.7/site-packages'), os.path.join(ROOT_PATH, 'sites')]
add_site_dir(ALLDIRS)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
