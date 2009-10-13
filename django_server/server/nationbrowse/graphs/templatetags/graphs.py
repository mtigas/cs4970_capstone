# coding=utf-8
from __future__ import division
from django import template
from django.template import resolve_variable
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode

from nationbrowse import graphs
from nationbrowse.graphs import graph_maker
from nationbrowse.demographics.models import PlacePopulation

from django.db.models.loading import get_model

register = template.Library()

@register.tag
def show_graph(parser,token):
    """
    Creates the image tag that renders a static (non-javascript) map.

    Usage:
        {% show_graph [place_type] [place.slug] [graph_type] %}
        {% show_graph county boone-missouri race_pie %}
        {% show_graph zipcode zip_obj.slug race_pie %}
    """
    try:
        # Get the tag's contents and parse it out into what we expect
        tag_name, place_type, slug, graph_type = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires three arguments: place_type, slug, graph_type" % tag_name
    return GraphHTMLNode(place_type, slug, graph_type)

class GraphHTMLNode(template.Node):
    def __init__(self, place_type, slug, graph_type):
        self.place_type = place_type
        self.slug = slug
        self.graph_type = graph_type

    def render(self, context):
        try:
            place_type = force_unicode(resolve_variable(self.place_type, context))
        except:
            place_type = force_unicode(self.place_type)

        try:
            slug = force_unicode(resolve_variable(self.slug, context))
        except:
            slug = force_unicode(self.slug)
        
        try:
            graph_type = force_unicode(resolve_variable(self.graph_type, context))
        except:
            graph_type = force_unicode(self.graph_type)
        
        try:
            PlaceClass = get_model("places",place_type)
            if not PlaceClass:
                return u""
            place = PlaceClass.objects.get(slug__iexact=slug)
            
            labels = getattr(graph_maker, '%s_labels' % graph_type)
            values = getattr(graph_maker, '%s_values' % graph_type)(place.population_demographics)
            colors = getattr(graph_maker, '%s_colors' % graph_type)
            total = getattr(graph_maker, '%s_total' % graph_type)(place.population_demographics)
            percents = map(lambda x: (x/total*100), values)
            
            graph_url = reverse("graphs:render_graph",args=(place_type,slug,graph_type,200),current_app="graphs")
            
            retstr = u'''<style type="text/css">
                .graph_label_icon{width:1em;height:1em;display:block;float:left;clear:left;border:1px solid #444;margin-right:5px;}
                .clear{clear:both}
                </style>
                '''
            
            for v in xrange(0,len(labels)):
                retstr = '%s\n<div class="graph_label_icon" style="background-color:%s;">&nbsp;</div> %s: %s (%1.2f%%)</span><br class="clear"/>' % (
                    retstr,
                    colors[v],
                    labels[v],
                    values[v],
                    percents[v]
                )
                
            
            return '\n<img src="%s"><br />\n%s' % (graph_url,retstr)
        except Exception:
            from traceback import print_exc
            print_exc
            return u""
    