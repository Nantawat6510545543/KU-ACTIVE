# To use Neon with Django, you have to create a Project on Neon
# and specify the project connection settings in your settings.py
# in the same way as for standalone Postgres.
import dj_database_url
from decouple import config
from mysite.settings import BASE_DIR

try:
    DATABASE_URL = config("DATABASE_URL", default=None)
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True
        )
    }
except ValueError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
