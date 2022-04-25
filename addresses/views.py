"""Views for the addresses app."""
from django.views.generic import TemplateView

from . import __version__ as app_version

# from django.utils.translation import gettext_lazy as _

# from . import models


class WelcomeAppView(TemplateView):
    template_name = 'addresses/welcome.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_version'] = app_version
        return context
