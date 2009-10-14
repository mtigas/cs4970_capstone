from django.core.cache import cache
from hashlib import sha512
from django.utils.encoding import smart_str

USING_MEMCACHED = (cache.__module__ == 'django.core.cache.backends.memcached')

def _get_real_cachename(cachename):
    """
    Memcached is picky about key names.  They have to be <= 250 characters and cannot contain whitespace
    or control characters.  This function creates "safe" keys by replacing those control characters and
    applying a SHA256 hash if the key is >250 chars long.
    
    Benefits:
        * Super long keys don't need to be truncated.  The hash function keeps them unique while shortening.
        * Cache contents cannot be introspected: this means cache data can't simply be browsed by key,
          which provides a little privacy protection if we are caching user-specific data.
    """
    # Only need this on memcached
    if not USING_MEMCACHED:
        return cachename
    
    cachename = cachename.replace('\n','\\n').replace('\r','\\r').replace('\t','\\t').replace(' ','\\_')
    cachename = smart_str(cachename,errors="backslashreplace")
    if len(cachename) > 250:
        # Concatenate part of the original string to avoid collisions and not waste the 250char limit
        cachename = "%s%s" % (cachename[:122], sha512(cachename).hexdigest())
    return cachename

def safe_get_cache(cachename):
    """ Gets an item from the cache (converting the given string into an always valid cache key) """
    return cache.get( _get_real_cachename(cachename) )

def safe_set_cache(cachename,obj,cachetime=None):
    """ Puts an item into the cache (converting the given string into an always valid cache key) """
    if cachetime is None:
        # Use the default cachetime from settings
        cache.set(
            _get_real_cachename(cachename),
            obj
        )
    else:
        cache.set(
            _get_real_cachename(cachename),
            obj,
            cachetime
        )
    return obj

def safe_del_cache(cachename):
    """ Deletes an item from the cache (converting the given string into an always valid cache key) """
    cache.delete( _get_real_cachename(cachename) )

# The following are based on work from http://fi.am/entry/low-level-cache-decorators-for-django/
def cached_method(func, cachetime=None):
    """ Decorator for plain methods """
    def cached_func(*args, **kwargs):
        key = 'cached_method_%s_%s_%s' % \
            (func.__name__, hash(args), hash(frozenset(kwargs.items())))
        val = safe_get_cache(key)
        return safe_set_cache(key, func(*args, **kwargs), cachetime) if val is None else val
    return cached_func

def cached_clsmethod(func, cachetime=None):
    """ Decorator for class methods """
    def cached_func(self, *args, **kwargs):
        key = 'cached_clsmethod_%s_%s_%s_%s_%s' % \
            (self.__class__.__name__, func.__name__, self.pk, hash(args), hash(frozenset(kwargs.items())))
        val = safe_get_cache(key)
        return safe_set_cache(key, func(self, *args, **kwargs), cachetime) if val is None else val
    return cached_func

def cached_property(func, cachetime=None):
    """ Decorator for class properties """
    def cached_func(self):
        key = 'cached_property_%s_%s_%s' % \
            (self.__class__.__name__, func.__name__, self.pk)
        val = safe_get_cache(key)
        return safe_set_cache(key, func(self), cachetime) if val is None else val
    return property(cached_func)
