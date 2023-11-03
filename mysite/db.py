# To use Neon with Django, you have to create a Project on Neon
# and specify the project connection settings in your settings.py
# in the same way as for standalone Postgres.
import dj_database_url
import logging

from decouple import config
from mysite.settings import BASE_DIR

# Configure the root logger (which logs to the console)
logging.basicConfig(level=logging.DEBUG)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

try:
    DATABASE_URL = config("DATABASE_URL", default=None)
    if DATABASE_URL not in [None, '']:
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True
            )
        }
    else:
        logging.warning("DATABASE_URL not found. Auto-migrating on local database.")
except ValueError:
    logging.warning("Invalid DATABASE_URL. Auto-migrating on local database.")
