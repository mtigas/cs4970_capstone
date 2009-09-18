from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django.template import resolve_variable
from django.utils.encoding import force_unicode
from cacheutil import safe_get_cache,safe_set_cache

register = Library()

class SafeCacheNode(Node):
    def __init__(self, nodelist, expire_time_var, fragment_name, vary_on):
        self.nodelist = nodelist
        self.expire_time_var = Variable(expire_time_var)
        self.fragment_name = fragment_name
        self.vary_on = vary_on

    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"safecache" tag got an unknkown variable: %r' % self.expire_time_var.var)
        try:
            expire_time = int(expire_time)
        except (ValueError, TypeError):
            raise TemplateSyntaxError('"safecache" tag got a non-integer timeout value: %r' % expire_time)
        
        # The cache name.
        cache_key = u':'.join([self.fragment_name])
        
        # The variables passed to the cache name.
        for var in self.vary_on:
            try:
                v = force_unicode(resolve_variable(var, context))
            except:
                v = "None"
            cache_key = "%s:%s=%s" % (cache_key,force_unicode(var),v)
        
        # Now work with the cache.
        try:
            value = safe_get_cache(cache_key)
        except:
            value = None
        if value is None:
            value = self.nodelist.render(context)
            safe_set_cache(cache_key, value, expire_time)
        return value

def do_safecache(parser, token):
    """
    This will cache the contents of a template fragment for a given amount
    of time.

    Usage::

        {% load safecache %}
        {% safecache [expire_time] [fragment_name] %}
            .. some expensive processing ..
        {% endcache %}

    This tag also supports varying by a list of arguments::

        {% load safecache %}
        {% safecache [expire_time] [fragment_name] [var1] [var2] .. %}
            .. some expensive processing ..
        {% safecache %}

    Each unique set of arguments will result in a unique cache entry.
    """
    nodelist = parser.parse(('endsafecache',))
    parser.delete_first_token()
    tokens = token.contents.split()
    if len(tokens) < 3:
        raise TemplateSyntaxError(u"'%r' tag requires at least 2 arguments." % tokens[0])
    return SafeCacheNode(nodelist, tokens[1], tokens[2], tokens[3:])

register.tag('safecache', do_safecache)
