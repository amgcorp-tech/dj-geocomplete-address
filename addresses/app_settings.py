from django.conf import settings

from addresses.utils.utils import discover_addresses_settings


GOOGLE_API_KEY = discover_addresses_settings()


USE_DJANGO_JQUERY = getattr(settings, "USE_DJANGO_JQUERY", False)
USE_JQUERY_V2 = getattr(settings, "USE_JQUERY_V2", False)
USE_JQUERY_V3 = getattr(settings, "USE_JQUERY_V3", False)

if USE_JQUERY_V2:
    JQUERY_URL2 = getattr(
        settings,
        "JQUERY_URL2",
        "https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js",
    )

if USE_JQUERY_V3:
    JQUERY_URL3 = getattr(
        settings,
        "JQUERY_URL3",
        "https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js",
    )





