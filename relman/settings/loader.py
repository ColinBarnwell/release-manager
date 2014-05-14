""" Load settings files based on environment variables """

from os import environ
from os.path import normpath
import sys


def get_env_setting(setting_name):
    """
    Get the environment setting or raise an exception.
    """
    try:
        return environ[setting_name]
    except KeyError:
        error_msg = "Environment variable %s is not set." % setting_name
        raise ImproperlyConfigured(error_msg)


# Import the common settings
from common import *

# Bring in the server-specific settings
execfile(normpath(join(DJANGO_ROOT, 'settings/servers/', get_env_setting('DJANGO_SERVER_SETTINGS'))))

# If we are running a test, switch out the DB for SQL lite and forget about migrations
if 'test' in sys.argv:
    SOUTH_TESTS_MIGRATE = False
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

# Load any additional server-specific apps
INSTALLED_APPS += ADDITIONAL_APPS
MIDDLEWARE_CLASSES += ADDITIONAL_MIDDLEWARE
