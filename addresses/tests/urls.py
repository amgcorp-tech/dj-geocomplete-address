"""URLs to run the tests."""
from django.contrib import admin
from django.urls import path, include
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.i18n import JavaScriptCatalog
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

last_modified_date = timezone.now()

# App Api urls here...
urlpatterns = [
    path('jsi18n/',
             cache_page(86400, key_prefix='js18n-%s' % last_modified_date)(
                 JavaScriptCatalog.as_view(packages=['addresses']),
             ), name='javascript-catalog'),
    path("select2/", include("django_select2.urls")),
    path('admin', admin.site.urls),
    path(
        "api/docs/", include_docs_urls(title="API Docs", public=True, permission_classes=(AllowAny,)),
    ),

    # Include app urls here...
    path('api/addresses/', include('addresses.api.urls')),
    path('', include('addresses.urls')),

]