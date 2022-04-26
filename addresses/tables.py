from django.utils.safestring import mark_safe
from django_tables2 import tables
from django_tables2.utils import AttributeDict
from django.utils.translation import gettext_lazy as _

from .models import State, Country, Region, Address

ACTIONS_ATTR = {"th": {"class": "text-center"}, "td": {"class": "text-center"}}
SELECTION_ATTR = {'class': "checkbox checkbox--brand"}


class CustomCheckboxColumn(tables.columns.CheckBoxColumn):

    @property
    def header(self):
        default = {"type": "checkbox"}

        general = self.attrs.get("input")
        specific = self.attrs.get("th__input")
        attrs = AttributeDict(default, **(specific or general or {}))

        input = "<input %s/ autocomplete='off'><span></span>" % attrs.as_html()
        header_attrs = AttributeDict(SELECTION_ATTR)
        label = f"<label {header_attrs.as_html()}>{input}</label>"

        return mark_safe(label)

    def render(self, value, bound_column, record):
        input = super(CustomCheckboxColumn, self).render(value, bound_column, record)
        # include span
        input = input + "<span></span>"
        attrs = AttributeDict(SELECTION_ATTR)
        label = f"<label {attrs.as_html()}>{input}</label>"

        return mark_safe(label)


class Selection(tables.Table):
    selection = CustomCheckboxColumn(accessor="id")


class TranslatedTable(tables.Table):
    def __init__(self, *args, **kwargs):
        super(TranslatedTable, self).__init__(*args, **kwargs)
        for column in self.base_columns:
            verbose = self.base_columns[column].verbose_name
            if verbose:
                self.base_columns[column].verbose_name = _(verbose)
            else:
                self.base_columns[column].verbose_name = _(column)


class CountryTable(Selection, TranslatedTable):
    name = tables.columns.RelatedLinkColumn(
        verbose_name=_("Name")
    )
    code = tables.columns.TemplateColumn(
        template_code="{{record.code}}",
        verbose_name=_("Code")
    )
    code3 = tables.columns.TemplateColumn(
        template_code="{{record.code3}}",
        verbose_name=_("Code3")
    )
    is_active = tables.columns.TemplateColumn(
        template_name="addresses/countries/table/table_boolean.html",
        verbose_name=_("Is active?")
    )

    actions = tables.columns.TemplateColumn(
        verbose_name=_("Actions"), template_name="addresses/countries/table/table_actions.html",
        orderable=False,
        # attrs=ACTIONS_ATTR
    )

    class Meta:
        model = Country
        fields = ("selection", "name", "code", "code3", "currency", "phone_code", "is_active", "actions")


class StateTable(Selection, TranslatedTable):
    name = tables.columns.RelatedLinkColumn(
        verbose_name=_("Name")

    )
    country = tables.columns.RelatedLinkColumn(
        verbose_name=_("Country")
    )
    code = tables.columns.TemplateColumn(
        template_code="{{record.code}}",
        verbose_name=_("Code")
    )
    actions = tables.columns.TemplateColumn(
        verbose_name=_("Actions"), template_name="addresses/states/table/table_actions.html",
        orderable=False,
    )

    class Meta:
        model = State
        fields = ("selection", "name", "country", "code", "actions")


class RegionsTable(Selection, TranslatedTable):
    name = tables.columns.RelatedLinkColumn(
        verbose_name=_("Name")
    )
    active = tables.columns.TemplateColumn(
        template_name="addresses/regions/table/table_boolean.html",
        verbose_name=_("Is active?")
    )
    actions = tables.columns.TemplateColumn(
        verbose_name=_("Actions"), template_name="addresses/regions/table/table_actions.html",
        orderable=False,
    )

    class Meta:
        model = Region
        fields = ("selection", "name", "total_countries", "active", "actions")


class AddressTable(Selection, TranslatedTable):
    formatted = tables.columns.RelatedLinkColumn(
        verbose_name=_("Name")
    )
    actions = tables.columns.TemplateColumn(
        verbose_name=_("Actions"), template_name="addresses/address/table/table_actions.html",
        orderable=False,
    )

    class Meta:
        model = Address
        fields = ("selection", "formatted", "latitude", "longitude", "actions")