# coding=utf-8
"""
This file defines the data models for our places.

 * PolyModel is an abstract class that the other places inherit. It gives
   subclasses some useful methods. Any algorithm that could apply on
   all polygonal models should go here.
 * State
 * County

To match up with Census-recorded data, we also store the FIPS code of most
of these objects - they come embedded in the Census' TIGER/Line data, which
is what populates these model tables.
 * See also http://en.wikipedia.org/wiki/Federal_Information_Processing_Standard
 * Note: ZIP codes do not have FIPS codes. The ZIP code itself acts as
   the "GEO_ID2" on Census tables.
"""

from django.conf import settings
from cacheutil import cached_clsmethod,cached_property,USING_DUMMY_CACHE
from django.db import models
from django_caching.models import CachedModel
from django_caching.managers import CachingManager

from nationbrowse.demographics.models import PlacePopulation,CrimeData,SocialCharacteristics
from django.contrib.gis.measure import Area
from django.contrib.contenttypes import generic
from threadutil import call_in_bg
import re

# Are we on a GIS-aware server?
USE_GIS = getattr(settings,'USE_GIS',False)

# If so, override some of the above imports
if USE_GIS:
    from django.contrib.gis.db import models
    from django_caching.models import GeoCachedModel as CachedModel
    from django_caching.managers import GeoCachingManager,PolyDeferGeoManager
    from django.contrib.gis.geos import fromstr as geo_from_str

# --------------------------------------------------------------

TRUNCATE_WKT = re.compile('(-?\d?\d?\d\.\d\d\d\d\d\d)(\d+)(,? ?)')

class PolyModel(CachedModel):
    """
    An abstract base class for any model with a polygon region.
    """
    name = models.CharField(max_length=250,db_index=True)
    slug = models.SlugField(unique=True,max_length=250,db_index=True)
    
    if USE_GIS:
        poly    = models.MultiPolygonField(verbose_name="geographic area data",blank=True,null=True)
    else:
        poly    = models.TextField(verbose_name="geographic area data (non-GIS)",blank=True,null=True)

    poly_source = "U.S. Census Bureau TIGER/Line, 2008"
    poly_source_url = "http://www.census.gov/geo/www/tiger/"

    def center(self):
        """
        Returns the Point that corresponds to the center of this object's shape.
        """
        if not self.poly:
            return None
        try:
            if isinstance(self.poly,basestring):
                return geo_from_str(self.poly).centroid
            else:
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
        if not USE_GIS:
            return None
        if not self.poly:
            return False
        
        point = geo_from_str("POINT(%s %s)" % (lon,lat))
        
        if isinstance(self.poly,basestring):
            return geo_from_str(self.poly).contains(point)
        else:
            return self.poly.contains(point)
    contains_coordinate = cached_clsmethod(contains_coordinate, 15552000)

    def simple_wkt(self):
        """
        Since most of our polygons are HORRIBLY detailed (~ 1 million chars for Missouri's
        WKT), we simplify it a bit and lose some of the detail (.01 tolerance -> 9000 chars
        for Missouri's WKT; .05 -> 2278 chars).
        
        Additionally uses a compiled regular expression to truncate coordinates to at most
        six decimal places.
        """
        if not USE_GIS:
            return None
        if not self.poly:
            return False
        
        simple = TRUNCATE_WKT.sub(
            r'\1\3',
            self.poly.simplify(tolerance=.01).wkt
        )
        
        # If that tolerance level results in an empty polygon (the algorithm
        # gets rid of too many points), try to do a "dumb" simplification on it.
        if simple == "POLYGON EMPTY":
            simple = TRUNCATE_WKT.sub(
                r'\1\3',
                self.poly.simplify(tolerance=.01,preserve_topology=True).wkt
            )
        
        # Try a "dumb" simplification on it.
        if simple == "POLYGON EMPTY":
            simple = TRUNCATE_WKT.sub(
                r'\1\3',
                self.poly.simplify().wkt
            )
        
        # Try a "dumb" simplification on it.
        if simple == "POLYGON EMPTY":
            simple = TRUNCATE_WKT.sub(
                r'\1\3',
                self.poly.simplify(preserve_topology=True).wkt
            )
        
        # If even *that* doesn't get a simple polygon, just return the standard poly,
        # with the coordinates truncated to 6 decimal places.
        if simple == "POLYGON EMPTY":
            simple = TRUNCATE_WKT.sub(
                r'\1\3',
                self.poly.wkt
            )
        
        return simple
    simple_wkt = cached_property(simple_wkt, 15552000)
    
    def area(self):
        """
        Since most of our polygons are HORRIBLY detailed (~ 1 million chars for Missouri's
        WKT), we simplify it a bit and lose some of the detail (.01 tolerance -> 9000 chars
        for Missouri's WKT; .05 -> 2278 chars).
        
        Additionally uses a compiled regular expression to truncate coordinates to at most
        six decimal places.
        """
        if not USE_GIS:
            return None
        if not self.poly:
            return False
        
        # Not the most exact, but it applies nationally.
        p = self.poly.transform(2163,True)
        return Area(sq_m=p.area,default_unit="sq_mi")
    area = cached_property(area, 15552000)
    
    # Special fake foreign keys to models within the Demographics app
    demographic_fkey = generic.GenericRelation(PlacePopulation, content_type_field='place_type', object_id_field='place_id')
    crime_fkey = generic.GenericRelation(CrimeData, content_type_field='place_type', object_id_field='place_id')
    socioeco_fkey = generic.GenericRelation(SocialCharacteristics, content_type_field='place_type', object_id_field='place_id')

    def population_demographics(self):
        """
        If this place has a record in PlacePopulation, retrieve and return that.
        """
        if self.demographic_fkey and self.demographic_fkey.count() > 0:
            try:
                return self.demographic_fkey.order_by('-source__date').all()[0]
            except:
                return None
    population_demographics = cached_property(population_demographics, 15552000)
    
    def crime_data(self):
        """
        If this place has a record in CrimeData, retrieve and return that.
        """
        if self.crime_fkey and self.crime_fkey.order_by('-source__date').count() > 0:
            try:
                return self.crime_fkey.all()[0]
            except:
                return None
    crime_data = cached_property(crime_data, 15552000)
    
    def socioeco_data(self):
        """
        If this place has a record in CrimeData, retrieve and return that.
        """
        if self.socioeco_fkey and self.socioeco_fkey.order_by('-source__date').count() > 0:
            try:
                return self.socioeco_fkey.all()[0]
            except:
                return None
    socioeco_data = cached_property(socioeco_data, 15552000)
    
    class Meta:
        abstract = True

# --------------------------------------------------------------

class Nation(PolyModel):
    if USE_GIS:
        objects = PolyDeferGeoManager()
        pobjects = GeoCachingManager()
    else:
        objects = CachingManager()
    
    def get_states(self):
        return State.objects.defer('poly',).all()
    states = cached_property(get_states, 15552000)
    children = cached_property(get_states, 15552000)
    
    parent = None
    
    class Meta:
        ordering = ('name',)
	
    def __unicode__(self):
        return u"%s" % (self.name)
    
    #@models.permalink
    #def get_absolute_url(self):
    #    return ('places:nation_detail', (), {
    #        'slug' : self.id
    #    })

class State(PolyModel):
    if USE_GIS:
        objects = PolyDeferGeoManager()
        pobjects = GeoCachingManager()
    else:
        objects = CachingManager()
    
    abbr     = models.CharField(verbose_name="abbreviation",max_length=10,help_text="Standard mailing abbreviation in CAPS; i.e. WA",db_index=True)
    ap_style = models.CharField(verbose_name="AP style",max_length=75,help_text="AP style abbreviation; i.e. Wash.")
    fips_code = models.PositiveSmallIntegerField(verbose_name="FIPS code",null=True,db_index=True)
    
    def get_counties(self):
        return self.county_set.defer('poly',).all()
    counties = cached_property(get_counties, 15552000)
    children = cached_property(get_counties, 15552000)
    
    def get_parent(self):
        return Nation.objects.get(id=1)
    parent = cached_property(get_parent, 15552000)
    
    class Meta:
        ordering = ('name',)
	
    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('places:state_detail', (), {
            'slug' : self.slug
        })

class County(PolyModel):
    if USE_GIS:
        objects = PolyDeferGeoManager()
        pobjects = GeoCachingManager()
    else:
        objects = CachingManager()
    
    state  = models.ForeignKey('State',db_index=True)
    fips_code = models.PositiveSmallIntegerField(verbose_name="FIPS code",null=True,db_index=True)
    long_name = models.CharField(max_length=100,help_text="full name or legal/statistical area description")
    
    csafp = models.PositiveIntegerField(verbose_name="Statistical Area Code",blank=True,null=True)
    cbsafp = models.PositiveIntegerField(verbose_name="Metropolitan Area Code",blank=True,null=True)
    metdivfp = models.PositiveIntegerField(verbose_name="Metropolitan Division Code",blank=True,null=True)

    def get_parent(self):
        return self.state
    parent = cached_property(get_parent, 15552000)
    children = []

    class Meta:
        verbose_name_plural = "counties"
        ordering = ('state','name',)
        unique_together = (('name', 'state'))
	
    def __unicode__(self):
        return u"%s, %s" % (self.long_name, self.state.name)
    __unicode__ = cached_clsmethod(__unicode__, 15552000)
    
    @models.permalink
    def get_absolute_url(self):
        return ('places:county_detail', (), {
            'state_abbr' : self.state.abbr.lower(),
            'name' : self.name.lower()
        })
