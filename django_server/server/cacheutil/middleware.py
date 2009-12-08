from django.core.cache import cache
from django.conf import settings
from django.utils.cache import get_max_age

class NginxMemcacheMiddleWare(object):
    """
    Similar to Django's cache middleware, except this operates on a set-only basis,
    to be used by the nginx memcached module <http://wiki.nginx.org/NginxHttpMemcachedModule>.
    
    See the following URL for details:
        <http://bretthoerner.com/blog/2008/oct/27/using-nginx-memcached-module-django/>
    """
    def process_response(self, request, response):
        # Get the path (do it early since we do conditionals on it)
        path = request.get_full_path()
        
        anon_only = getattr(settings,"CACHE_MIDDLEWARE_ANONYMOUS_ONLY",False)
        
        # A few conditions that cause us not to cache.
        if request.method != "GET" \
          or not response.status_code == 200:
            return response
        
        # The cache key prefix (should match what is in the site's nginx config)
        prefix = getattr(settings,"NGINX_CACHE_PREFIX","NG")
        
        # See the value of max-age and set timer on that. If not set,
        # use CACHE_MIDDLEWARE_SECONDS. If 0, do not cache.
        timeout = get_max_age(response)
        if timeout == None:
            timeout = getattr(settings,"CACHE_MIDDLEWARE_SECONDS",300)
        elif timeout == 0:
            return response
        
        # Set the item in cache.
        key = "%s:%s" % (prefix, path)
        cache.set(key, response._get_content(), timeout)
        
        return response
