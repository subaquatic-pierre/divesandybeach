from django.forms.widgets import Select
from django.template import loader
from django.utils.safestring import mark_safe


class KitSelectWidget(Select):
    template_name = 'diving/widgets/kit_select.html'

    # def get_context(self, name, value, attrs=None):
    #     return {'widget': {
    #             'name': name,
    #             'choices': choices
    #             }}

    # def render(self, name, value, attrs=None):
    #     context = self.get_context(name, value, choices, attrs)
    #     template = loader.get_template(self.template_name).render(context)
    #     return mark_safe(template)


class CertLevelSelectWidget(Select):
    template_name = 'diving/widgets/cert_level_select.html'

    # def get_context(self, name, value, attrs=None):
    #     return {'widget': {
    #             'name': name,
    #             'choices': choices
    #             }}

    # def render(self, name, value, attrs=None):
    #     context = self.get_context(name, value, choices, attrs)
    #     template = loader.get_template(self.template_name).render(context)
    #     return mark_safe(template)
