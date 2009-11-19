# coding=utf-8
from django.db import models

from cacheutil import cached_clsmethod
from django_caching.models import CachedModel
from django_caching.managers import CachingManager

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from datetime import date

class DataSource(CachedModel):
    """ Stores metadata regarding a particular source of demographic information """
    objects = CachingManager()
    
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

class PlacePopulation(CachedModel):
    """
    Each record represents data from one source, for one particular place.
    
    For example, PlacePopulation.objects.get(pk=24703) gets you the Census 2000 population data
    for ZipCode 65201.
    """
    objects = CachingManager()
    
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
    
    @property
    def total_mixed(self):
        return self.tworace + self.threerace + self.fourrace + self.fiverace + self.sixrace
    
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
    
    # Alternate properties (so ages can be bracketed by five year intervals
    # since some of the given data has more specific intervals)
    @property
    def male_15_19(self):
        return self.male_15_17 + self.male_18_19
    @property
    def male_20_24(self):
        return self.male_20 + self.male_21 + self.male_22_24
    @property
    def male_60_64(self):
        return self.male_60_61 + self.male_62_64
    @property
    def male_65_69(self):
        return self.male_65_66 + self.male_67_69
    
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

    # Alternate properties (so ages can be bracketed by five year intervals
    # since some of the given data has more specific intervals)
    @property
    def female_15_19(self):
        return self.female_15_17 + self.female_18_19
    @property
    def female_20_24(self):
        return self.female_20 + self.female_21 + self.female_22_24
    @property
    def female_60_64(self):
        return self.female_60_61 + self.female_62_64
    @property
    def female_65_69(self):
        return self.female_65_66 + self.female_67_69

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
    
    # Alternate properties (so ages can be bracketed by five year intervals
    # since some of the given data has more specific intervals)
    @property
    def age_15_19(self):
        return self.age_15_17 + self.age_18_19
    @property
    def age_20_24(self):
        return self.age_20 + self.age_21 + self.age_22_24
    @property
    def age_60_64(self):
        return self.age_60_61 + self.age_62_64
    @property
    def age_65_69(self):
        return self.age_65_66 + self.age_67_69
    
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
        unique_together = (('place_type','place_id','source'),)
	
    def __unicode__(self):
        return u"%s population demographics" % (self.place)
    __unicode__ = cached_clsmethod(__unicode__, 604800)
    
    age_fields = [
        # field, shortname, longname
        ("age_0_4","0-4","0-4 years old"),
        ("age_5_9","5-9","5-9 years old"),
        ("age_10_14","10-14","10-14 years old"),
        ("age_15_19","15-19","15-19 years old"),
        ("age_20_24","20-24","20-24 years old"),
        ("age_25_29","25-29","25-29 years old"),
        ("age_30_34","30-34","30-34 years old"),
        ("age_35_39","35-39","35-39 years old"),
        ("age_40_44","40-44","40-44 years old"),
        ("age_45_49","45-49","45-49 years old"),
        ("age_50_54","50-54","50-54 years old"),
        ("age_55_59","55-59","55-59 years old"),
        ("age_60_64","60-64","60-64 years old"),
        ("age_65_69","65-69","65-69 years old"),
        ("age_70_74","70-74","70-74 years old"),
        ("age_75_79","75-79","75-79 years old"),
        ("age_80_84","80-84","80-84 years old"),
        ("age_85_plus","85+","85+ years old")
    ]

class CrimeData(CachedModel):
    objects = CachingManager()
    
    place_type = models.ForeignKey(ContentType)
    place_id = models.PositiveIntegerField(db_index=True)
    place = generic.GenericForeignKey(ct_field='place_type',fk_field='place_id')
    
    source = models.ForeignKey(DataSource,db_index=True)
    
    """
    UCR Table 1  = violent crimes, national
    UCR Table 5  = violent crimes, by state
    UCR Table 10 = violent crimes, by county
    """
    violent_crime = models.PositiveIntegerField(default=0,db_index=True)
    murder = models.PositiveIntegerField("murders and nonnegligent manslaughter",default=0,db_index=True)
    rape = models.PositiveIntegerField("forcible rape",default=0,db_index=True)
    robbery = models.PositiveIntegerField(default=0,db_index=True)
    assault = models.PositiveIntegerField("aggravated assault",default=0,db_index=True)
    
    property_crime = models.PositiveIntegerField(default=0,db_index=True)
    burglary = models.PositiveIntegerField(default=0,db_index=True)
    larceny_theft = models.PositiveIntegerField("larceny-theft",default=0,db_index=True)
    auto_theft = models.PositiveIntegerField("motor vehicle theft",default=0,db_index=True)
    
    """
    UCR Table 77 = Law enforcement employees, by state
    UCR Table 80 = Law enforcement employees, by county
    """
    law_enforcement_employees = models.PositiveIntegerField("total law enforcement employees",default=0,db_index=True)
    male_officers = models.PositiveIntegerField(default=0,db_index=True)
    female_officers = models.PositiveIntegerField(default=0,db_index=True)
    male_civilians = models.PositiveIntegerField("male civilian employees",default=0,db_index=True)
    female_civilians = models.PositiveIntegerField("female civilian employees",default=0,db_index=True)
    employing_agencies = models.PositiveIntegerField("number of employing agencies",default=0,db_index=True)
    
    class Meta:
        verbose_name = "crime data"
        verbose_name_plural = "crime data"
        ordering = ('place_type','place_id')
        unique_together = (('place_type','place_id','source'),)
	
    def __unicode__(self):
        return u"%s crime data" % (self.place)
    __unicode__ = cached_clsmethod(__unicode__, 604800)

"""
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