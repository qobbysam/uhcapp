import os
from uhcapp.settings.base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

all_environ = os.environ.get('ALLOWED_HOSTS')

ALLOWED_HOSTS = all_environ.split(",")  


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}


Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}


# Q_CLUSTER = {
#     'redis': {
#         'host': os.environ.get('REDISHOST'),
#         'port': os.environ.get('REDISPORT'),
#         'db': os.environ.get('REDISDB'),
#         'password': os.environ.get('REDISPASSWORD'),
#         'socket_timeout': None,
#         'charset': 'utf-8',
#         'errors': 'strict',
#         'unix_socket_path': None
#     }
# }

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


#choose whoosh but elastic search is better for perfomance
import os
WHOOSH = os.path.join(BASE_DIR, 'whoosh')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH },
}
