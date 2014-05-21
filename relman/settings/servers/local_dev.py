""" Server-specific settings for local development """


########## DEBUG CONFIGURATION

DEBUG = True
TEMPLATE_DEBUG = DEBUG

########## END DEBUG CONFIGURATION


########## ADMIN CONFIGURATION

ADMINS = (
)

MANAGERS = ADMINS

########## END ADMIN CONFIGURATION


########## SECRET CONFIGURATION

SECRET_KEY = 'GENERATE_A_KEY_BEFORE_DEPLOYING_TO_PRODUCTION!'

########## END SECRET CONFIGURATION


########## MIDDLEWARE CONFIGURATION

ADDITIONAL_MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

########## END MIDDLEWARE CONFIGURATION


########## APP CONFIGURATION

ADDITIONAL_APPS = (
    'debug_toolbar',
)

# DEBUG TOOLBAR
INTERNAL_IPS = ('10.0.2.2')

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

########## END APP CONFIGURATION


########## DATABASE CONFIGURATION

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dev_relman',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        'DEFAULT_STORAGE_ENGINE': 'INNODB',
    },
}


########## END DATABASE CONFIGURATION


########## SERVER CONFIGURATION

TIME_ZONE = 'Europe/London'

CACHE_BACKEND = 'locmem:///'

########## END SERVER CONFIGURATION


########## EMAIL CONFIGURATION

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

########## END EMAIL CONFIGURATION
