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
from cacheutil import cached_clsmethod,cached_property,USING_DUMMY_CACHE
from django.db import models

from nationbrowse.demographics.models import PlacePopulation
from django.contrib.contenttypes import generic
from threadutil import call_in_bg

# Are we on a GIS-aware server?
USE_GIS = getattr(settings,'USE_GIS',False)

# If so, override some of the above imports
if USE_GIS:
    from django.contrib.gis.db import models
    from django.contrib.gis.geos import fromstr as geo_from_str

    class PolyDeferGeoManager(models.Manager):
        def get_query_set(self):
            return models.query.GeoQuerySet(self.model).defer('poly',)

# --------------------------------------------------------------

class PolyModel(models.Model):
    """
    An abstract base class for any model with a polygon region.
    """
    name = models.CharField(max_length=250,db_index=True)
    slug = models.SlugField(unique=True,max_length=250,db_index=True)
    
    if USE_GIS:
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
    
    # Special fake foreign key that checks the PlacePopulation table for a record
    # that corresponds with this Place.
    demographic_fkey = generic.GenericRelation(PlacePopulation, content_type_field='place_type', object_id_field='place_id')
    
    def population_demographics(self):
        """
        If this place has a record in PlacePopulation, retrieve and return that.
        """
        if self.demographic_fkey and self.demographic_fkey.count() > 0:
            try:
                return self.demographic_fkey.all()[0]
            except:
                return None
    population_demographics = cached_property(population_demographics, 15552000)

    class Meta:
        abstract = True

# --------------------------------------------------------------

class State(PolyModel):
    if USE_GIS:
        objects = PolyDeferGeoManager()
        pobjects = models.Manager()
    
    abbr     = models.CharField(verbose_name="abbreviation",max_length=10,help_text="Standard mailing abbreviation in CAPS; i.e. WA",db_index=True)
    ap_style = models.CharField(verbose_name="AP style",max_length=75,help_text="AP style abbreviation; i.e. Wash.")
    fips_code = models.PositiveSmallIntegerField(verbose_name="FIPS code",null=True,db_index=True)
    
    def counties(self):
        if self.county_set.count() > 0:
            return self.county_set.iterator()
        else:
            return None
    
    def zipcodes(self):
        if self.zipcode_set.count() > 0:
            return self.zipcode_set.iterator()
        else:
            return None
    
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
        pobjects = models.Manager()
    
    state  = models.ForeignKey('State',db_index=True)
    fips_code = models.PositiveSmallIntegerField(verbose_name="FIPS code",null=True,db_index=True)
    long_name = models.CharField(max_length=100,help_text="full name or legal/statistical area description")
    
    csafp = models.PositiveIntegerField(verbose_name="Statistical Area Code",blank=True,null=True)
    cbsafp = models.PositiveIntegerField(verbose_name="Metropolitan Area Code",blank=True,null=True)
    metdivfp = models.PositiveIntegerField(verbose_name="Metropolitan Division Code",blank=True,null=True)

    #def zipcodes(self):
    #    if USE_GIS:
    #        return ZipCode.objects.filter(poly__intersects=self.poly)
    #    else:
    #        return None
    #zipcodes = cached_property(zipcodes, 15552000)
    
    class Meta:
        verbose_name_plural = "counties"
        ordering = ('name',)
        unique_together = (('name', 'state'))
	
    def __unicode__(self):
        return u"%s, %s" % (self.name, self.state.name)
    __unicode__ = cached_clsmethod(__unicode__, 1800)
    
    @models.permalink
    def get_absolute_url(self):
        return ('places:county_detail', (), {
            'state_abbr' : self.state.abbr.lower(),
            'name' : self.name.lower()
        })

class ZipCode(PolyModel):
    if USE_GIS:
        objects = PolyDeferGeoManager()
        pobjects = models.Manager()

    # Technically, ZipCodes can span multiple states. We're only storing the "primary" match.
    state  = models.ForeignKey('State',blank=True,null=True,db_index=True)

    #def counties(self):
    #    if USE_GIS:
    #        return County.objects.filter(state=self.state,poly__intersects=self.poly)
    #    else:
    #        return None
    #counties = cached_property(counties, 15552000)

    #def county(self):
    #    """
    #    If this ZIP code belongs to a county, returns that.
    #    If it belongs to more than one county, returns the first match.
    #    Otherwise, returns None.
    #    """
    #    if USE_GIS:
    #        c = self.counties
    #        if c and (c.count() > 0):
    #            return c[0]
    #        else:
    #            return None
    #    else:
    #        return None
    #county = cached_property(county, 15552000)

    class Meta:
        ordering = ('name',)
        db_table = "places_zipcode2"
	
    def __unicode__(self):
        return u"%s" % (self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('places:zipcode_detail', (), {
            'slug' : self.id
        })

"""
Used for converting data from tl_2008_us_zcta5.shp, imported via:
ogr2ogr -f PostgreSQL "PG:dbname=cs4970_capstone" -nlt MULTIPOLYGON -t_srs EPSG:4326 -overwrite tl_2008_us_zcta5.shp

See also management/commands/import_zipcode.py

class ConversionZipCode(models.Model):
    id = models.PositiveIntegerField(db_column="ogc_fid",primary_key=True)
    wkb_geometry = models.MultiPolygonField(verbose_name="geographic area data",blank=True,null=True)
    zipcode_x = models.CharField(max_length=5,blank=True,null=True,db_column="zcta5ce")

    @cached_property
    def zipcode(self):
        a = self.zipcode_x.strip()
        if a.isdigit():
            return a
        else:
            return None
        
    def __unicode__(self):
        return u"%s" % self.zipcode
    __unicode__ = cached_clsmethod(__unicode__, 1800)

    class Meta:
        db_table = 'tl_2008_us_zcta5'
"""         

"""
Used for converting data from tl_2008_us_county.shp, imported via:
ogr2ogr -f PostgreSQL "PG:dbname=cs4970_capstone" -nlt MULTIPOLYGON -t_srs EPSG:4326 -skipfailures -overwrite tl_2008_us_county.shp
Import failures were handled manually (some Puerto Rico Municipios had non-ASCII chars, causing ogr2ogr to throw warnings)

See also management/commands/import_counties.py
        
class ConversionCounty(models.Model):
    id = models.PositiveIntegerField(db_column="ogc_fid",primary_key=True)
    wkb_geometry = models.MultiPolygonField(verbose_name="geographic area data",blank=True,null=True)
    statefp = models.CharField(max_length=2,blank=True,null=True)
    countyfp = models.CharField(max_length=3,blank=True,null=True)
    name_x = models.CharField(max_length=100,blank=True,null=True,db_column='name')
    namelsad_x = models.CharField(max_length=100,blank=True,null=True,db_column='namelsad')
    csafp = models.CharField(verbose_name="Statistical Area Code",max_length=3,blank=True,null=True)
    cbsafp = models.CharField(verbose_name="Metropolitan Area Code",max_length=5,blank=True,null=True)
    metdivfp = models.CharField(verbose_name="Metropolitan Division Code",max_length=5,blank=True,null=True)

    @cached_property
    def name(self):
        if self.name_x.strip():
            return self.name_x.strip()
        else:
            return self.namelsad.replace(" Municipio","")

    @cached_property
    def namelsad(self):
        return self.namelsad_x.strip()

    def __unicode__(self):
        return u"%s" % self.namelsad
    __unicode__ = cached_clsmethod(__unicode__, 1800)

    class Meta:
        db_table = 'tl_2008_us_county'
"""