# coding=utf-8
from __future__ import division
from django import template
from django.conf import settings
from django.contrib.humanize.templatetags import humanize

from nationbrowse import graphs
from nationbrowse.graphs import googleGraphs as google_graphs
from nationbrowse.demographics.models import *

from django.db.models.loading import get_model

register = template.Library()

@register.tag
def show_on_map(parser,token):
    try:
        tag_name, place_type, slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments: place_type, slug" % tag_name
    return StaticMapHTMLNode(place_type, slug)

class StaticMapHTMLNode(template.Node):
    def __init__(self, place_type, slug):
        self.place_type = place_type
        self.slug = slug
    
    def render(self, context):
        try:
            place_type = template.resolve_variable(self.place_type, context)
        except:
            place_type = self.place_type
        
        try:
            slug = template.resolve_variable(self.slug, context)
        except:
            slug = self.slug
                
        try:
            PlaceClass = get_model("places",place_type)
            if not PlaceClass:
                return ""
            place = PlaceClass.objects.get(slug__iexact=slug)
            
            if place_type == 'state':
                return '\n<img src="http://chart.apis.google.com/chart?cht=t&chs=400x200&chd=s:_&chtm=usa&chco=BBBBBB,000066,0000FF&chld=%s&chd=t:100">' % (
                    place.abbr
                )
            elif place.center:
                return '\n<img src="http://maps.google.com/maps/api/staticmap?markers=color:blue|%s,%s&center=%s,%s&zoom=5&maptype=terrain&size=300x200&key=%s&sensor=false">' % (
                    place.latitude,
                    place.longitude,
                    place.latitude,
                    place.longitude,
                    settings.GOOGLE_MAPS_API_KEY
                )
            else:
                return ""
        except Exception:
            from traceback import print_exc
            print_exc()
            return ""

@register.tag
def race_piechart(parser,token):
    """
    Creates the image tag that renders a static (non-javascript) map.

    Usage:
        {% race_piechart [place_type] [place.slug] %}
        {% race_piechart county boone-missouri %}
        {% race_piechart zipcode zip_obj.slug %}
    """
    try:
        # Get the tag's contents and parse it out into what we expect
        tag_name, place_type, slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments: place_type, slug" % tag_name
    return RacePiechartNode(place_type, slug)

class RacePiechartNode(template.Node):
    def __init__(self, place_type, slug):
        self.place_type = place_type
        self.slug = slug

    def render(self, context):
        try:
            place_type = template.resolve_variable(self.place_type, context)
        except:
            place_type = self.place_type

        try:
            slug = template.resolve_variable(self.slug, context)
        except:
            slug = self.slug
        
        try:
            PlaceClass = get_model("places",place_type)
            if not PlaceClass:
                return ""
            place = PlaceClass.objects.get(slug=slug)
            
            # Labels, values, and colors for each race.
            labels = [
                "White",
                "Black",
                "Native American",
                "Asian",
                "Pacific Islander",
                "Other",
                "Mixed descent",
            ]
            values = [
                place.population_demographics.onerace_white,
                place.population_demographics.onerace_black,
                place.population_demographics.onerace_amerindian,
                place.population_demographics.onerace_asian,
                place.population_demographics.onerace_pacislander,
                place.population_demographics.onerace_other,
                place.population_demographics.total_mixed
            ]
            colors = graphs.COLORS7
            
            google_graph_url = google_graphs.pie_chart(values, labels, colors, size=(400,200))
            
            # Generate an HTML output legend (where the box shows the color corresponding to the chart). i.e.:
            # [] White: 115714 (87.11%)
            # [] Black: 11572 (8.71%)
            # ...
            total = sum(values)
            percents = map(lambda x: (x/total*100.0), values)
            percents = map(lambda x: "%.2f"%x, percents)
            
            legend = ''
            for v in xrange(0,len(labels)):
                legend += '\n<div class="graph_label_icon" style="background-color:%s;">&nbsp;</div> %s: %s (%s%%)<br class="clear"/>' % (
                    colors[v],
                    labels[v],
                    humanize.intcomma(values[v]),
                    percents[v]
                )
            
            # Add some CSS so the legends look right.
            # Throw in the <img> tag for the Google Chart.
            return """<style type="text/css">
                .graph_label_icon{width:1em;height:1em;display:block;float:left;clear:left;border:1px solid #444;margin-right:5px;}
                .clear{clear:both}
                </style>
                <p><img src="%s"></p>%s""" % (google_graph_url, legend) 
        except Exception:
            from traceback import print_exc
            print_exc()
            return ""

@register.tag
def age_barchart(parser,token):
    """
    Creates the image tag that renders a static (non-javascript) map.

    Usage:
        {% age_barchart [place_type] [place.slug] %}
        {% age_barchart county boone-missouri %}
        {% age_barchart zipcode zip_obj.slug %}
    """
    try:
        # Get the tag's contents and parse it out into what we expect
        tag_name, place_type, slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments: place_type, slug" % tag_name
    return AgeBarchartNode(place_type, slug)

class AgeBarchartNode(template.Node):
    def __init__(self, place_type, slug):
        self.place_type = place_type
        self.slug = slug

    def render(self, context):
        try:
            place_type = template.resolve_variable(self.place_type, context)
        except:
            place_type = self.place_type

        try:
            slug = template.resolve_variable(self.slug, context)
        except:
            slug = self.slug
        
        try:
            PlaceClass = get_model("places",place_type)
            if not PlaceClass:
                return ""
            place = PlaceClass.objects.get(slug=slug)
            
            # Labels, values, and colors for each race.
            field_names, labels, nul = zip(*PlacePopulation.field_descriptions)
            values = map(lambda field_name: getattr(place.population_demographics,field_name), field_names)
            
            x_labels = ('0-4','','','15-17','','','21','','','30-34','','','45-49','','','60-61','','','67-69','','','','85%2B')
                
            google_graph_url = google_graphs.bar_chart(values, x_labels=x_labels, size=(400,200))
            
            # Generate an HTML output legend (where the box shows the color corresponding to the chart). i.e.:
            # [] White: 115714 (87.11%)
            # [] Black: 11572 (8.71%)
            # ...
            total = sum(values)
            percents = map(lambda x: (x/total*100.0), values)
            percents = map(lambda x: "%.2f"%x, percents)
            
            legend = ''
            for v in xrange(0,len(labels)):
                legend += '\n%s: %s (%s%%)<br class="clear"/>' % (
                    labels[v],
                    humanize.intcomma(values[v]),
                    percents[v]
                )
            
            # Add some CSS so the legends look right.
            # Throw in the <img> tag for the Google Chart.
            return """<style type="text/css">
                .graph_label_icon{width:1em;height:1em;display:block;float:left;clear:left;border:1px solid #444;margin-right:5px;}
                .clear{clear:both}
                </style>
                <p><img src="%s"></p>%s""" % (google_graph_url, legend) 
        except Exception:
            from traceback import print_exc
            print_exc()
            return ""
