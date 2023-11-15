# To use Neon with Django, you have to create a Project on Neon
# and specify the project connection settings in your settings.py
# in the same way as for standalone Postgres.
import dj_database_url
import logging
import sys

from decouple import config


def configure_database_settings(BASE_DIR):
    """
    Configure database settings for a Django application based on the provided BASE_DIR.

    Args:
        BASE_DIR (Path): The base directory of the Django project.

    Returns:
        dict: A dictionary containing the database settings, including the ENGINE and NAME.
              The specific database settings are determined based on the current environment.

    Note:
        - If running tests (identified by the 'test' argument in sys.argv), the function returns
          settings for the local SQLite database.
        - If a valid DATABASE_URL environment variable is found, it configures the database
          using the settings from the DATABASE_URL.
        - If DATABASE_URL is not found or invalid, it falls back to the local SQLite database.

    """
    local_database = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    testing = sys.argv[1:2] == ['test']
    if testing:
        logging.debug('Running tests on the local database.')
        return local_database

    try:
        database_url = config("DATABASE_URL", default=None)
        if database_url:
            cloud_database = {
                'default': dj_database_url.config(
                    default=database_url,
                    conn_max_age=0,
                    conn_health_checks=True,
                    ssl_require=True
                )
            }
            logging.info("Using a valid DATABASE_URL. Connecting to the Neon.")
            return cloud_database
        else:
            logging.info(
                "DATABASE_URL not found. Falling back to the local database.")
    except ValueError:
        logging.warning(
            "Invalid DATABASE_URL. Falling back to the local database.")

    return local_database
