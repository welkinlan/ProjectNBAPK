__author__ = 'tianlan'
from django import template

register = template.Library()

@register.filter(name='rank')
def rank(value, arg):
    return int(value)+(int(arg)-1)*10


@register.filter(name='int_equal')
def int_equal(value, arg):
    return int(value) == int(arg)