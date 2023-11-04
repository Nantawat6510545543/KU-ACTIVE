# To use Neon with Django, you have to create a Project on Neon
# and specify the project connection settings in your settings.py
# in the same way as for standalone Postgres.
import dj_database_url
import logging
import sys

from decouple import config
from mysite.settings import BASE_DIR


def configure_database_settings():
    local_database = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    testing = sys.argv[1:2] == ['test']
    if testing:
        print('Running tests on the local database.')
        return local_database

    try:
        database_url = config("DATABASE_URL", default=None)
        if database_url not in [None, '']:
            return {
                'default': dj_database_url.config(
                    default=database_url,
                    conn_max_age=600,
                    conn_health_checks=True
                )
            }
        else:
            print(
                "DATABASE_URL not found. Auto-migrating on the local database.")
    except ValueError:
        logging.warning(
            "Invalid DATABASE_URL. Auto-migrating on the local database.")

    return local_database


DATABASES = configure_database_settings()
