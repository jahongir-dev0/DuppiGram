from django import template

register = template.Library()

@register.filter
def getattr_filter(obj, attr_name):
    """Obyekt ichidan atributni dinamik olish"""
    return getattr(obj, attr_name, None)
