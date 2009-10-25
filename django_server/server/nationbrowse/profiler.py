import sys
import tempfile
import cProfile
import pstats
from django.conf import settings
from cStringIO import StringIO
import os

class ProfileMiddleware(object):
    def process_request(self, request):
        if (request.META.get('REMOTE_ADDR','') in settings.INTERNAL_IPS) or (request.GET.has_key('prof')):
            self.profiler = cProfile.Profile()
            self.tmpfile = tempfile.NamedTemporaryFile()
    
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if (request.META.get('REMOTE_ADDR','') in settings.INTERNAL_IPS) or (request.GET.has_key('prof')):
            return self.profiler.runcall(callback, request, *callback_args, **callback_kwargs)
    
    def process_response(self, request, response):
        if (request.META.get('REMOTE_ADDR','') in settings.INTERNAL_IPS) or (request.GET.has_key('prof')):
            self.profiler.create_stats()

            out = StringIO()
            old_stdout = sys.stdout
            sys.stdout = out
            
            self.profiler.dump_stats(self.tmpfile.name)
            
            stats = pstats.Stats(self.tmpfile.name)
            
            stats.sort_stats('time')
            stats.strip_dirs()
            stats.print_stats()
            #print "\n\n" + ("-"*10)
            #stats.print_callees()

            sys.stdout = old_stdout
            
            profile_log = os.path.join(settings.DJANGO_SERVER_DIR, 'static', 'media', 'profiler_log.txt')
            f=open(profile_log,"a")
            f.write(request.path + "\n\n" + out.getvalue() + "\n\n" + ("="*20) +"\n\n")
            f.close()
        
        return response
