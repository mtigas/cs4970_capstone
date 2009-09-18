import managers
import fields
from django.db import models

class CachedModel(models.Model):
    from_cache = False
    class Meta:
        abstract = True

# ------------------ custom code, adds support for geo: --------------------
from django.conf import settings
if ('django.contrib.gis' in settings.INSTALLED_APPS):
    from django.contrib.gis.db import models as geo_models

    class GeoCachedModel(geo_models.Model):
        from_cache = False
        class Meta:
            abstract = True
