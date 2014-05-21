""" Server-specific settings for local development """


########## DEBUG CONFIGURATION

DEBUG = False
TEMPLATE_DEBUG = DEBUG

########## END DEBUG CONFIGURATION


########## ADMIN CONFIGURATION

ADMINS = (
    ('Colin Barnwell', 'cbarnwell@twig-world.com'),
)

MANAGERS = ADMINS

########## END ADMIN CONFIGURATION


########## SECRET CONFIGURATION

SECRET_KEY = 'f4)4(p_idl#!x6rlvxyg@_h+p2_5k&t#f)a=o^i5gxkns&@dk='

########## END SECRET CONFIGURATION


########## MIDDLEWARE CONFIGURATION

ADDITIONAL_MIDDLEWARE = (
)

########## END MIDDLEWARE CONFIGURATION


########## APP CONFIGURATION

ADDITIONAL_APPS = (
)

########## END APP CONFIGURATION


########## DATABASE CONFIGURATION

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'live_relman',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        'DEFAULT_STORAGE_ENGINE': 'INNODB',
    },
}


########## END DATABASE CONFIGURATION


########## SERVER CONFIGURATION

TIME_ZONE = 'Europe/Dublin'

CACHE_BACKEND = 'locmem:///'

########## END SERVER CONFIGURATION


########## EMAIL CONFIGURATION

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

########## END EMAIL CONFIGURATION
