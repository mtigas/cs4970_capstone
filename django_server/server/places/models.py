# coding=utf-8
"""
This file defines the data models for our places.

 * PolyModel is an abstract class that the other places inherit. It gives
   subclasses some useful methods. Any algorithm that could apply on
   all polygonal models should go here.
 * State
 * County
 * ZipCode

To match up with Census-recorded data, we also store the FIPS code of most
of these objects - they come embedded in the Census' TIGER/Line data, which
is what populates these model tables.
 * See also http://en.wikipedia.org/wiki/Federal_Information_Processing_Standard
 * Note: ZIP codes do not have FIPS codes. The ZIP code itself acts as
   the "GEO_ID2" on Census tables.
"""

from django.conf import settings
from cacheutil import cached_clsmethod,cached_property
from django.db import models
from django_caching.models import CachedModel
from django_caching.managers import CachingManager

# Are we on a GIS-aware server?
USE_GEODJANGO = ('django.contrib.gis' in settings.INSTALLED_APPS)

# If so, override some of the above imports
if USE_GEODJANGO:
    from django.contrib.gis.db import models
    from django_caching.models import GeoCachedModel as CachedModel
    from django_caching.managers import GeoCachingManager,PolyDeferGeoManager
    from django.contrib.gis.geos import fromstr as geo_from_str

# --------------------------------------------------------------

class PolyModel(models.Model):
    """
    An abstract base class for any model with a polygon region.
    """
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    
    if USE_GEODJANGO:
        poly    = models.MultiPolygonField(verbose_name="geographic area data",blank=True,null=True)
    else:
        poly    = models.TextField(verbose_name="geographic area data (non-GIS)",blank=True,null=True)
    
    def center(self):
        """
        Returns the Point that corresponds to the center of this object's shape.
        """
        if not self.poly:
            return None
        try:
            return self.poly.centroid
        except:
            return None
    center = cached_property(center, 15552000)
    
    @property
    def latitude(self):
        """
        Returns the latitude for this objects' geographic center.
        """
        if not self.center:
            return None
        
        return self.center.y
    
    @property
    def longitude(self):
        """
        Returns the longitude for this objects' geographic center.
        """
        if not self.center:
            return None
        
        return self.center.x

    def contains_coordinate(self, lat, lon):
        """ Helper method; given a lat/lon, returns whether the given point is within this PolyModel. """
        if not USE_GEODJANGO:
            return None
        if not self.poly:
            return False
        
        point = geo_from_str("POINT(%s %s)" % (lon,lat))
        return self.poly.contains(point)
    contains_coordinate = cached_clsmethod(contains_coordinate, 15552000)
    
    class Meta:
        abstract = True

# --------------------------------------------------------------

class State(PolyModel):
    if USE_GEODJANGO:
        objects = GeoCachingManager()
        dobjects = PolyDeferGeoManager()
    else:
        objects = CachingManager()
    
    abbr     = models.CharField(verbose_name="abbreviation",max_length=10,help_text="Standard mailing abbreviation in CAPS; i.e. WA")
    ap_style = models.CharField(verbose_name="AP style",max_length=75,help_text="AP style abbreviation; i.e. Wash.")
    fips_code = models.PositiveSmallIntegerField(verbose_name="FIPS code",null=True)
    
    class Meta:
        ordering = ('name',)
	
    def __unicode__(self):
        return unicode(self.name)
        
class County(PolyModel):
    if USE_GEODJANGO:
        objects = GeoCachingManager()
        dobjects = PolyDeferGeoManager()
    else:
        objects = CachingManager()
    
    state  = models.ForeignKey('State',max_length=75)
    fips_code = models.PositiveSmallIntegerField(verbose_name="FIPS code",null=True)
    long_name = models.CharField(max_length=100,help_text="full name or legal/statistical area description")
    
    class Meta:
        verbose_name_plural = "counties"
        ordering = ('name',)
        unique_together = (('name', 'state'))
	
    def __unicode__(self):
        return u"%s, %s" % (self.name, self.state.name)
    __unicode__ = cached_clsmethod(__unicode__, 1800)

class ZipCode(PolyModel):
    if USE_GEODJANGO:
        objects = GeoCachingManager()
        dobjects = PolyDeferGeoManager()
    else:
        objects = CachingManager()
	
    # Allow blank/null: ZIP codes don't always belong to a state (cross state lines, or US military)
    state = models.ForeignKey('State',blank=True,null=True)
    
    class Meta:
        ordering = ('name',)
	
    def __unicode__(self):
        if self.state:
            return u"%s, %s" % (self.name, self.state.name)
        else:
            return u"%s" % (self.name)
    __unicode__ = cached_clsmethod(__unicode__, 1800)
