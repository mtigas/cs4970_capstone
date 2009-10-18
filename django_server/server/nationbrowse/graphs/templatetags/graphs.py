# coding=utf-8
from django import template
from django.template import resolve_variable
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
from urllib import urlencode

from nationbrowse import graphs
from nationbrowse.graphs import graph_maker
from nationbrowse.demographics.models import PlacePopulation

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
            place_type = force_unicode(resolve_variable(self.place_type, context))
        except:
            place_type = force_unicode(self.place_type)
        
        try:
            slug = force_unicode(resolve_variable(self.slug, context))
        except:
            slug = force_unicode(self.slug)
                
        try:
            PlaceClass = get_model("places",place_type)
            if not PlaceClass:
                return u""
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
                return u""
        except Exception:
            from traceback import print_exc
            print_exc()
            return u""


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
        
        # Only implement race_pie graph chart for now.
        if "race_pie" not in graph_type:
            print "wat"
            return ""
        
        try:
            PlaceClass = get_model("places",place_type)
            if not PlaceClass:
                return ""
            place = PlaceClass.objects.get(slug=slug)
            
            # This needs a SERIOUS refactor.
            # Just assume that labels, values, and colors all return lists
            # where labels[0] is the label for the population number in values[0]
            # and likewise for colors[0].
            labels = getattr(graph_maker, '%s_labels' % graph_type)
            values = getattr(graph_maker, '%s_values' % graph_type)(place.population_demographics)
            colors = getattr(graph_maker, '%s_colors' % graph_type)
            
            # Google Charts pie chart does not like huge numbers, so turn these into percents (from 0-100)
            total = sum(values)
            percents = map(lambda x: (float(x)/float(total)*100.0), values)
            
            # The resulting `percents` list is a list of floats. Cast these as 
            # formatted strings, so we can "join" the sequence when we output the string.
            # Only go to two decimal points when formatting the string.
            percents = map(lambda x: "%.2f"%x, percents)
            
            # Build the request parameters as a dictionary so we can use urllib.urlencode
            # to create a nice and safe string.
            request_parameters = {
                'cht':"p",
                'chs':"400x200"
            }
            
            # Chart data is percents list as a comma-delimited string starting with "t:"
            # i.e.: chd=t:8.75,1.1,10.2
            request_parameters['chd'] = "t:" + ",".join(percents)
            
            # Labels is pipe-delimited.
            request_parameters['chl'] = "|".join(labels)
            
            # Colors is pipe-delimited. We also remove leading # from hex colors since
            # google takes the hex value straight up.
            request_parameters['chco'] = "|".join(map(lambda x: x.replace("#",'').upper(), colors))
            
            # The URL, hooray.
            google_graph_url = "http://chart.apis.google.com/chart?%s" % urlencode(request_parameters)
            
            # Generate an HTML output legend (where the box shows the color corresponding to the chart). i.e.:
            # [] White: 115714 (87.11%)
            # [] Black: 11572 (8.71%)
            # ...
            legend = ''
            for v in xrange(0,len(labels)):
                legend += '\n<div class="graph_label_icon" style="background-color:%s;">&nbsp;</div> %s: %s (%s%%)</span><br class="clear"/>' % (
                    colors[v],
                    labels[v],
                    values[v],
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
