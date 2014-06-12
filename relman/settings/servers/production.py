""" Server-specific settings for deployment """


########## DEBUG CONFIGURATION

DEBUG = False
TEMPLATE_DEBUG = DEBUG

########## END DEBUG CONFIGURATION


########## ADMIN CONFIGURATION

ADMINS = (
    # Add an admin
)

MANAGERS = ADMINS

########## END ADMIN CONFIGURATION


########## SECRET CONFIGURATION

SECRET_KEY = 'GENERATE_A_SECRET_KEY'

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
