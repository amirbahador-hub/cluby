from .base import *

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

try:
    INSTALLED_APPS += ['debug_toolbar', 'django_extensions']
    MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
        ]
    INTERNAL_IPS = ["127.0.0.1"]

except ImportError as ex:
    print(ex)



