"""Templatetags for the addresses app."""
from django import template

from addresses.utils.utils import get_sidebar_template_context

register = template.Library()


@register.inclusion_tag('addresses/inc/sidebar_menu.html', takes_context=True)
def render_addresses_menu(context):
    template_context = get_sidebar_template_context(context)
    return template_context
