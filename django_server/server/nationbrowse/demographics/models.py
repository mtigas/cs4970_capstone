# coding=utf-8
from django.db import models

from cacheutil import cached_clsmethod

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from datetime import date

class DataSource(models.Model):
    """ Stores metadata regarding a particular source of demographic information """
    source = models.CharField(max_length=255)
    date = models.DateField(help_text="Note that for some data sources, only the year is valid.")
    url = models.URLField(blank=True,null=True,max_length=255,verify_exists=False)
    
    @property
    def name(self):
        return u"%s" % (self.source)
    
    def __unicode__(self):
        return u"%s, %s" % (self.source, self.date.year)
    
    class Meta:
        ordering = ('date','source')
        unique_together = (('source','date'),)

class PlacePopulation(models.Model):
    """
    Each record represents data from one source, for one particular place.
    
    For example, PlacePopulation.objects.get(pk=24703) gets you the Census 2000 population data
    for ZipCode 65201.
    """
    # Internal Django fields that handles the GenericForeignKey below
    place_type = models.ForeignKey(ContentType)
    place_id = models.PositiveIntegerField(db_index=True)
    
    # References one of the models (State, County, ZipCode) in our Places app
    place = generic.GenericForeignKey(ct_field='place_type',fk_field='place_id')
    
    # To future-proof for things like Census 2010
    source = models.ForeignKey(DataSource,db_index=True)
    
    # Census P1 = Total Population
    total = models.PositiveIntegerField(default=0,db_index=True)
    
    # Census P2 = Urban & Rural Population
    urban = models.PositiveIntegerField(default=0,db_index=True)
    rural = models.PositiveIntegerField(default=0,db_index=True)
    
    # Census P3 = Race
    onerace = models.PositiveIntegerField(default=0,db_index=True)
    onerace_white = models.PositiveIntegerField(default=0,db_index=True)
    onerace_black = models.PositiveIntegerField(default=0,db_index=True)
    onerace_amerindian = models.PositiveIntegerField(default=0,db_index=True)
    onerace_asian = models.PositiveIntegerField(default=0,db_index=True)
    onerace_pacislander = models.PositiveIntegerField(default=0,db_index=True)
    onerace_other = models.PositiveIntegerField(default=0,db_index=True)
    tworace = models.PositiveIntegerField(default=0,db_index=True)
    threerace = models.PositiveIntegerField(default=0,db_index=True)
    fourrace = models.PositiveIntegerField(default=0,db_index=True)
    fiverace = models.PositiveIntegerField(default=0,db_index=True)
    sixrace = models.PositiveIntegerField(default=0,db_index=True)
    
    # Census P9 = Race (Tallied)
    white = models.PositiveIntegerField("White, alone or in combination with other races",default=0,db_index=True)
    black = models.PositiveIntegerField("African American, alone or in combination with other races",default=0,db_index=True)
    amerindian = models.PositiveIntegerField("American Indian, alone or in combination with other races",default=0,db_index=True)
    asian = models.PositiveIntegerField("Asian, alone or in combination with other races",default=0,db_index=True)
    pacislander = models.PositiveIntegerField("Hawaiian or Pacific Islander, alone or in combination with other races",default=0,db_index=True)
    other = models.PositiveIntegerField("Some other race, alone or in combination with other races",default=0,db_index=True)
    
    # Census P12 = Gender, by age
    male = models.PositiveIntegerField(default=0,db_index=True)
    male_0_4 = models.PositiveIntegerField(default=0,db_index=True)
    male_5_9 = models.PositiveIntegerField(default=0,db_index=True)
    male_10_14 = models.PositiveIntegerField(default=0,db_index=True)
    male_15_17 = models.PositiveIntegerField(default=0,db_index=True)
    male_18_19 = models.PositiveIntegerField(default=0,db_index=True)
    male_20 = models.PositiveIntegerField(default=0,db_index=True)
    male_21 = models.PositiveIntegerField(default=0,db_index=True)
    male_22_24 = models.PositiveIntegerField(default=0,db_index=True)
    male_25_29 = models.PositiveIntegerField(default=0,db_index=True)
    male_30_34 = models.PositiveIntegerField(default=0,db_index=True)
    male_35_39 = models.PositiveIntegerField(default=0,db_index=True)
    male_40_44 = models.PositiveIntegerField(default=0,db_index=True)
    male_45_49 = models.PositiveIntegerField(default=0,db_index=True)
    male_50_54 = models.PositiveIntegerField(default=0,db_index=True)
    male_55_59 = models.PositiveIntegerField(default=0,db_index=True)
    male_60_61 = models.PositiveIntegerField(default=0,db_index=True)
    male_62_64 = models.PositiveIntegerField(default=0,db_index=True)
    male_65_66 = models.PositiveIntegerField(default=0,db_index=True)
    male_67_69 = models.PositiveIntegerField(default=0,db_index=True)
    male_70_74 = models.PositiveIntegerField(default=0,db_index=True)
    male_75_79 = models.PositiveIntegerField(default=0,db_index=True)
    male_80_84 = models.PositiveIntegerField(default=0,db_index=True)
    male_85_plus = models.PositiveIntegerField(default=0,db_index=True)
    female = models.PositiveIntegerField(default=0,db_index=True)
    female_0_4 = models.PositiveIntegerField(default=0,db_index=True)
    female_5_9 = models.PositiveIntegerField(default=0,db_index=True)
    female_10_14 = models.PositiveIntegerField(default=0,db_index=True)
    female_15_17 = models.PositiveIntegerField(default=0,db_index=True)
    female_18_19 = models.PositiveIntegerField(default=0,db_index=True)
    female_20 = models.PositiveIntegerField(default=0,db_index=True)
    female_21 = models.PositiveIntegerField(default=0,db_index=True)
    female_22_24 = models.PositiveIntegerField(default=0,db_index=True)
    female_25_29 = models.PositiveIntegerField(default=0,db_index=True)
    female_30_34 = models.PositiveIntegerField(default=0,db_index=True)
    female_35_39 = models.PositiveIntegerField(default=0,db_index=True)
    female_40_44 = models.PositiveIntegerField(default=0,db_index=True)
    female_45_49 = models.PositiveIntegerField(default=0,db_index=True)
    female_50_54 = models.PositiveIntegerField(default=0,db_index=True)
    female_55_59 = models.PositiveIntegerField(default=0,db_index=True)
    female_60_61 = models.PositiveIntegerField(default=0,db_index=True)
    female_62_64 = models.PositiveIntegerField(default=0,db_index=True)
    female_65_66 = models.PositiveIntegerField(default=0,db_index=True)
    female_67_69 = models.PositiveIntegerField(default=0,db_index=True)
    female_70_74 = models.PositiveIntegerField(default=0,db_index=True)
    female_75_79 = models.PositiveIntegerField(default=0,db_index=True)
    female_80_84 = models.PositiveIntegerField(default=0,db_index=True)
    female_85_plus = models.PositiveIntegerField(default=0,db_index=True)

    # Derived from above set:
    age_0_4 = models.PositiveIntegerField(default=0,db_index=True)
    age_5_9 = models.PositiveIntegerField(default=0,db_index=True)
    age_10_14 = models.PositiveIntegerField(default=0,db_index=True)
    age_15_17 = models.PositiveIntegerField(default=0,db_index=True)
    age_18_19 = models.PositiveIntegerField(default=0,db_index=True)
    age_20 = models.PositiveIntegerField(default=0,db_index=True)
    age_21 = models.PositiveIntegerField(default=0,db_index=True)
    age_22_24 = models.PositiveIntegerField(default=0,db_index=True)
    age_25_29 = models.PositiveIntegerField(default=0,db_index=True)
    age_30_34 = models.PositiveIntegerField(default=0,db_index=True)
    age_35_39 = models.PositiveIntegerField(default=0,db_index=True)
    age_40_44 = models.PositiveIntegerField(default=0,db_index=True)
    age_45_49 = models.PositiveIntegerField(default=0,db_index=True)
    age_50_54 = models.PositiveIntegerField(default=0,db_index=True)
    age_55_59 = models.PositiveIntegerField(default=0,db_index=True)
    age_60_61 = models.PositiveIntegerField(default=0,db_index=True)
    age_62_64 = models.PositiveIntegerField(default=0,db_index=True)
    age_65_66 = models.PositiveIntegerField(default=0,db_index=True)
    age_67_69 = models.PositiveIntegerField(default=0,db_index=True)
    age_70_74 = models.PositiveIntegerField(default=0,db_index=True)
    age_75_79 = models.PositiveIntegerField(default=0,db_index=True)
    age_80_84 = models.PositiveIntegerField(default=0,db_index=True)
    age_85_plus = models.PositiveIntegerField(default=0,db_index=True)
    
    # P15 Households
    # P16 Population in Households
    # P17 Avg household size
    num_households = models.PositiveIntegerField(default=0,db_index=True)
    pop_in_households = models.PositiveIntegerField(default=0,db_index=True)
    avg_household_size = models.DecimalField(max_digits=4, decimal_places=2, db_index=True)

    # P31 Families
    # P32 Population in families
    # P33 Avg family size
    num_families = models.PositiveIntegerField(default=0,db_index=True)
    pop_in_families = models.PositiveIntegerField(default=0,db_index=True)
    avg_family_size = models.DecimalField(max_digits=4, decimal_places=2, db_index=True)
    
    class Meta:
        verbose_name = "population set"
        verbose_name_plural = "population sets"
        ordering = ('place_type','place_id')
        unique_together = (('place_type','place_id'),)
	
    def __unicode__(self):
        return u"%s population demographics" % (self.place)
    __unicode__ = cached_clsmethod(__unicode__, 1800)


"""
Used for converting data from tl_2008_us_county.shp. Process:
 * Create model
 * Perform syncdb to create table.
 * Remove top two lines of dc_dec_2000_sf1_u_data1.txt
 * Replace all || with |0| in dc_dec_2000_sf1_u_data1.txt
 * For counties, non-ASCII characters needed to be replaced (in Puerto Rican region names)
 * in dbshell,
   * COPY dc_dec_2000_sf1 (geo_id,geo_id2,sumlevel,geo_name,p001001,p002001,p002002,p002003,p002004,p002005,
     p002006,p003001,p003002,p003003,p003004,p003005,p003006,p003007,p003008,p003009,p003010,p003011,p003012,
     p003013,p003014,p003015,p003016,p003017,p003018,p003019,p003020,p003021,p003022,p003023,p003024,p003025,
     p003026,p003027,p003028,p003029,p003030,p003031,p003032,p003033,p003034,p003035,p003036,p003037,p003038,
     p003039,p003040,p003041,p003042,p003043,p003044,p003045,p003046,p003047,p003048,p003049,p003050,p003051,
     p003052,p003053,p003054,p003055,p003056,p003057,p003058,p003059,p003060,p003061,p003062,p003063,p003064,
     p003065,p003066,p003067,p003068,p003069,p003070,p003071,p009001,p009002,p009003,p009004,p009005,p009006,
     p009007,p012001,p012002,p012003,p012004,p012005,p012006,p012007,p012008,p012009,p012010,p012011,p012012,
     p012013,p012014,p012015,p012016,p012017,p012018,p012019,p012020,p012021,p012022,p012023,p012024,p012025,
     p012026,p012027,p012028,p012029,p012030,p012031,p012032,p012033,p012034,p012035,p012036,p012037,p012038,
     p012039,p012040,p012041,p012042,p012043,p012044,p012045,p012046,p012047,p012048,p012049,p015001,p016001,
     p017001,p031001,p032001,p033001) from '/tmp/dc_dec_2000_sf1_u_data1.txt' WITH DELIMITER '|';

State, County, and ZipCode demographic data were done one at a time (and this table dropped after each import,
because this table was used for each import.

See the scripts under management/commands/convert_*_data.py to see how this was converted into PlacePopulation.



class PopulationImport(models.Model):
    geo_id = models.CharField(max_length=255)
    fips_code = models.CharField(max_length=5,db_column="geo_id2")
    sumlevel = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255,db_column="geo_name")
    p001001 = models.PositiveIntegerField(default=0)
    p002001 = models.PositiveIntegerField(default=0)
    p002002 = models.PositiveIntegerField(default=0)
    p002003 = models.PositiveIntegerField(default=0)
    p002004 = models.PositiveIntegerField(default=0)
    p002005 = models.PositiveIntegerField(default=0)
    p002006 = models.PositiveIntegerField(default=0)
    p003001 = models.PositiveIntegerField(default=0)
    p003002 = models.PositiveIntegerField(default=0)
    p003003 = models.PositiveIntegerField(default=0)
    p003004 = models.PositiveIntegerField(default=0)
    p003005 = models.PositiveIntegerField(default=0)
    p003006 = models.PositiveIntegerField(default=0)
    p003007 = models.PositiveIntegerField(default=0)
    p003008 = models.PositiveIntegerField(default=0)
    p003009 = models.PositiveIntegerField(default=0)
    p003010 = models.PositiveIntegerField(default=0)
    p003011 = models.PositiveIntegerField(default=0)
    p003012 = models.PositiveIntegerField(default=0)
    p003013 = models.PositiveIntegerField(default=0)
    p003014 = models.PositiveIntegerField(default=0)
    p003015 = models.PositiveIntegerField(default=0)
    p003016 = models.PositiveIntegerField(default=0)
    p003017 = models.PositiveIntegerField(default=0)
    p003018 = models.PositiveIntegerField(default=0)
    p003019 = models.PositiveIntegerField(default=0)
    p003020 = models.PositiveIntegerField(default=0)
    p003021 = models.PositiveIntegerField(default=0)
    p003022 = models.PositiveIntegerField(default=0)
    p003023 = models.PositiveIntegerField(default=0)
    p003024 = models.PositiveIntegerField(default=0)
    p003025 = models.PositiveIntegerField(default=0)
    p003026 = models.PositiveIntegerField(default=0)
    p003027 = models.PositiveIntegerField(default=0)
    p003028 = models.PositiveIntegerField(default=0)
    p003029 = models.PositiveIntegerField(default=0)
    p003030 = models.PositiveIntegerField(default=0)
    p003031 = models.PositiveIntegerField(default=0)
    p003032 = models.PositiveIntegerField(default=0)
    p003033 = models.PositiveIntegerField(default=0)
    p003034 = models.PositiveIntegerField(default=0)
    p003035 = models.PositiveIntegerField(default=0)
    p003036 = models.PositiveIntegerField(default=0)
    p003037 = models.PositiveIntegerField(default=0)
    p003038 = models.PositiveIntegerField(default=0)
    p003039 = models.PositiveIntegerField(default=0)
    p003040 = models.PositiveIntegerField(default=0)
    p003041 = models.PositiveIntegerField(default=0)
    p003042 = models.PositiveIntegerField(default=0)
    p003043 = models.PositiveIntegerField(default=0)
    p003044 = models.PositiveIntegerField(default=0)
    p003045 = models.PositiveIntegerField(default=0)
    p003046 = models.PositiveIntegerField(default=0)
    p003047 = models.PositiveIntegerField(default=0)
    p003048 = models.PositiveIntegerField(default=0)
    p003049 = models.PositiveIntegerField(default=0)
    p003050 = models.PositiveIntegerField(default=0)
    p003051 = models.PositiveIntegerField(default=0)
    p003052 = models.PositiveIntegerField(default=0)
    p003053 = models.PositiveIntegerField(default=0)
    p003054 = models.PositiveIntegerField(default=0)
    p003055 = models.PositiveIntegerField(default=0)
    p003056 = models.PositiveIntegerField(default=0)
    p003057 = models.PositiveIntegerField(default=0)
    p003058 = models.PositiveIntegerField(default=0)
    p003059 = models.PositiveIntegerField(default=0)
    p003060 = models.PositiveIntegerField(default=0)
    p003061 = models.PositiveIntegerField(default=0)
    p003062 = models.PositiveIntegerField(default=0)
    p003063 = models.PositiveIntegerField(default=0)
    p003064 = models.PositiveIntegerField(default=0)
    p003065 = models.PositiveIntegerField(default=0)
    p003066 = models.PositiveIntegerField(default=0)
    p003067 = models.PositiveIntegerField(default=0)
    p003068 = models.PositiveIntegerField(default=0)
    p003069 = models.PositiveIntegerField(default=0)
    p003070 = models.PositiveIntegerField(default=0)
    p003071 = models.PositiveIntegerField(default=0)
    p009001 = models.PositiveIntegerField(default=0)
    p009002 = models.PositiveIntegerField(default=0)
    p009003 = models.PositiveIntegerField(default=0)
    p009004 = models.PositiveIntegerField(default=0)
    p009005 = models.PositiveIntegerField(default=0)
    p009006 = models.PositiveIntegerField(default=0)
    p009007 = models.PositiveIntegerField(default=0)
    p012001 = models.PositiveIntegerField(default=0)
    p012002 = models.PositiveIntegerField(default=0)
    p012003 = models.PositiveIntegerField(default=0)
    p012004 = models.PositiveIntegerField(default=0)
    p012005 = models.PositiveIntegerField(default=0)
    p012006 = models.PositiveIntegerField(default=0)
    p012007 = models.PositiveIntegerField(default=0)
    p012008 = models.PositiveIntegerField(default=0)
    p012009 = models.PositiveIntegerField(default=0)
    p012010 = models.PositiveIntegerField(default=0)
    p012011 = models.PositiveIntegerField(default=0)
    p012012 = models.PositiveIntegerField(default=0)
    p012013 = models.PositiveIntegerField(default=0)
    p012014 = models.PositiveIntegerField(default=0)
    p012015 = models.PositiveIntegerField(default=0)
    p012016 = models.PositiveIntegerField(default=0)
    p012017 = models.PositiveIntegerField(default=0)
    p012018 = models.PositiveIntegerField(default=0)
    p012019 = models.PositiveIntegerField(default=0)
    p012020 = models.PositiveIntegerField(default=0)
    p012021 = models.PositiveIntegerField(default=0)
    p012022 = models.PositiveIntegerField(default=0)
    p012023 = models.PositiveIntegerField(default=0)
    p012024 = models.PositiveIntegerField(default=0)
    p012025 = models.PositiveIntegerField(default=0)
    p012026 = models.PositiveIntegerField(default=0)
    p012027 = models.PositiveIntegerField(default=0)
    p012028 = models.PositiveIntegerField(default=0)
    p012029 = models.PositiveIntegerField(default=0)
    p012030 = models.PositiveIntegerField(default=0)
    p012031 = models.PositiveIntegerField(default=0)
    p012032 = models.PositiveIntegerField(default=0)
    p012033 = models.PositiveIntegerField(default=0)
    p012034 = models.PositiveIntegerField(default=0)
    p012035 = models.PositiveIntegerField(default=0)
    p012036 = models.PositiveIntegerField(default=0)
    p012037 = models.PositiveIntegerField(default=0)
    p012038 = models.PositiveIntegerField(default=0)
    p012039 = models.PositiveIntegerField(default=0)
    p012040 = models.PositiveIntegerField(default=0)
    p012041 = models.PositiveIntegerField(default=0)
    p012042 = models.PositiveIntegerField(default=0)
    p012043 = models.PositiveIntegerField(default=0)
    p012044 = models.PositiveIntegerField(default=0)
    p012045 = models.PositiveIntegerField(default=0)
    p012046 = models.PositiveIntegerField(default=0)
    p012047 = models.PositiveIntegerField(default=0)
    p012048 = models.PositiveIntegerField(default=0)
    p012049 = models.PositiveIntegerField(default=0)
    p015001 = models.PositiveIntegerField(default=0)
    p016001 = models.PositiveIntegerField(default=0)
    p017001 = models.DecimalField(max_digits=4, decimal_places=2)
    p031001 = models.PositiveIntegerField(default=0)
    p032001 = models.PositiveIntegerField(default=0)
    p033001 = models.DecimalField(max_digits=4, decimal_places=2)
    class Meta:
        db_table = "dc_dec_2000_sf1"
"""