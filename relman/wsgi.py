import os
import sys
from os.path import abspath, dirname
from django.core.handlers.wsgi import WSGIHandler


def application(environ, start_response):

    os.environ['DJANGO_SETTINGS_MODULE'] = environ['DJANGO_SETTINGS_MODULE']
    os.environ['DJANGO_SERVER_SETTINGS'] = environ['DJANGO_SERVER_SETTINGS']

    PROJECT_ROOT = dirname(dirname(abspath(__file__)))
    sys.path.append(PROJECT_ROOT)

    return WSGIHandler()(environ, start_response)
