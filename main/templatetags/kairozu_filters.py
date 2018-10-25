
from django import template
register = template.Library()

# @register.filter(name='cut')
# def cut(value, arg):    # e.g. {{ somevalue|cut:"0" }} 0 is the arg, somevalue is the value
#    """Removes all values of arg from the given string"""
#    return value.replace(arg, '')

# @register.filter
# def lower(value): # Only one argument.
#    """Converts a string into all lowercase"""
#    return value.lower()


@register.filter('supto')
def supto(value, upto):
    return value[0:upto]

@register.filter('addstr')
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)