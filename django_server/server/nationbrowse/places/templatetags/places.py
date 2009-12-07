# coding=utf-8
from __future__ import division
from django import template
from django.contrib.humanize.templatetags import humanize

register = template.Library()

@register.tag
def population_percent(parser,token):
    try:
        tag_name, place, number = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments: place, number" % tag_name
    return PopPercentNode(place, number)

def is_numeric(value):
    try:
        x = float(value)
    except ValueError:
        return False
    else:
        return True

class PopPercentNode(template.Node):
    def __init__(self, place, number):
        self.place = place
        self.number = number
    
    def render(self, context):
        try:
            place = template.resolve_variable(self.place, context)
        except:
            return ""
        
        try:
            number = template.resolve_variable(self.number, context)
        except:
            number = self.number
        if not is_numeric(number):
            return ""
        
        return "%.2f%%" % ((number / place.population_demographics.total) * 100)
