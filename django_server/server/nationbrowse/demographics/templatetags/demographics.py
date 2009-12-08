# coding=utf-8
from __future__ import division
from django import template
from django.contrib.humanize.templatetags import humanize
from django.template.defaultfilters import floatformat
from nationbrowse.demographics import get_data_aggregates

register = template.Library()

@register.tag
def data_aggregates(parser,token):
    try:
        tag_name, place, table, fieldname, aggregate_type = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires four arguments: place, table, fieldname, aggregate_type" % tag_name
    return AggregateDataNode(place, table, fieldname, aggregate_type)

class AggregateDataNode(template.Node):
    def __init__(self, place, table, fieldname, aggregate_type):
        self.place = place
        self.table = table
        self.fieldname = fieldname
        self.aggregate_type = aggregate_type
            
    def render(self, context):
        try:
            place = template.resolve_variable(self.place, context)
        except:
            return ""
        
        try:
            table = template.resolve_variable(self.table, context)
        except:
            table = self.table
            
        try:
            fieldname = template.resolve_variable(self.fieldname, context)
        except:
            fieldname = self.fieldname
            
        data = get_data_aggregates(
            place,
            table,
            fieldname
        )
        
        if (not data) or (not data.has_key(self.aggregate_type)):
            return ""
        
        return "%s" % humanize.intcomma(data[self.aggregate_type])



@register.tag
def data_agg_columns(parser,token):
    try:
        tag_name, place, table, fieldname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires three arguments: place, table, fieldname" % tag_name
    return AggregateColumnsNode(place, table, fieldname)

class AggregateColumnsNode(template.Node):
    def __init__(self, place, table, fieldname):
        self.place = place
        self.table = table
        self.fieldname = fieldname
            
    def render(self, context):
        try:
            place = template.resolve_variable(self.place, context)
        except:
            return "<td colspan='5' style='text-align:center;border-left:2px solid #999'>not available</td>"

        try:
            table = template.resolve_variable(self.table, context)
        except:
            table = self.table
            
        try:
            fieldname = template.resolve_variable(self.fieldname, context)
        except:
            fieldname = self.fieldname
        
        try:
            data = get_data_aggregates(
                place,
                table,
                fieldname
            )
        except:
            data = None
        
        if not data:
            return "<td colspan='5' style='text-align:center;border-left:2px solid #999'>not available</td>"
        
        return """
            <td style="text-align:right;border-left:2px solid #999">%s</td>
            <td style="text-align:right">%s</td>
            <td style="text-align:right">%s</td>
            <td style="text-align:right">%s</td>
            <td style="text-align:right">%s</td>""" % (
                humanize.intcomma(data['max']),
                humanize.intcomma(floatformat(data['avg'], 2)),
                humanize.intcomma(data['min']),
                humanize.intcomma(floatformat(data['stddev'], 2)),
                humanize.intcomma(data['variance'])
            )
