"""
These settings are used by the ``manage.py`` command.

With normal tests we want to use the fastest possible way which is an
in-memory sqlite database but if you want to create South migrations you
need a persistant database.

"""
from .test_settings import *  # NOQA

from django.contrib import messages
from decouple import config as env_config

REQUIRED_APPS = [
    "django_select2",
    "django_tables2",
    "django_filters",
    "widget_tweaks",
]


INSTALLED_APPS = INSTALLED_APPS + REQUIRED_APPS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}

# DJANGO_TABLES2
DJANGO_TABLES2_TEMPLATE = "metronic/backend/tables2/template.html"

# messages
MESSAGE_TAGS = {
    messages.DEBUG: "bg-secondary secondary",
    messages.INFO: "bg-info border-info",
    messages.SUCCESS: "bg-success border-success",
    messages.WARNING: "bg-warning border-warning",
    messages.ERROR: "bg-danger border-danger",
}

GOOGLE_API_KEY = env_config('GOOGLE_API_KEY', None)