from django.conf import settings
def api_key(request):    
    return {
        'GOOGLE_MAPS_API_KEY': getattr(settings,"GOOGLE_MAPS_API_KEY","")
    }
