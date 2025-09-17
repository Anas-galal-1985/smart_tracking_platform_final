# accounts/templatetags/form_tags.py
from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    if isinstance(field, BoundField):
        return field.as_widget(attrs={"class": css})
    return field  # إذا لم يكن BoundField أرجع كما هو
