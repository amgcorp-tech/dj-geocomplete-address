import os

from django.conf import settings


def discover_addresses_settings():
    GOOGLE_API_KEY = 'GOOGLE_API_KEY'


    if GOOGLE_API_KEY in os.environ:
        return os.environ[GOOGLE_API_KEY]

    if hasattr(settings, GOOGLE_API_KEY):
        return settings.GOOGLE_API_KEY

    raise AttributeError(
        "Could not find {google_api_key} in environment variables, or django project settings.".format(
            google_api_key=GOOGLE_API_KEY,
        )
    )


def load_version():
    import addresses as app
    return app.__version__


def get_sidebar_template_context(context):
    data = {
        'request': context['request'],
        'perms': context.get('perms', None)
    }

    return data
