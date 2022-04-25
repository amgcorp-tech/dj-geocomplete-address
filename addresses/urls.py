"""URLs for the addresses app."""
from django.urls import path

from . import views


urlpatterns = [
    path('',
        views.WelcomeAppView.as_view(),
        name='addresses_default'),
]
