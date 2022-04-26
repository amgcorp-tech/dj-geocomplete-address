from django.conf import settings

from addresses.utils.utils import discover_addresses_settings


GOOGLE_API_KEY = discover_addresses_settings()


USE_DJANGO_JQUERY = getattr(settings, "USE_DJANGO_JQUERY", False)
JQUERY_URL = getattr(
    settings,
    "JQUERY_URL",
    # "https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js",
    "https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js",
)






