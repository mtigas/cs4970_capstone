# coding=utf-8
from django.db import models

from cacheutil import cached_clsmethod
from django_caching.models import CachedModel
from django_caching.managers import CachingManager

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from datetime import date
from decimal import Decimal

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
    """
    objects = CachingManager()
    
    # Internal Django fields that handles the GenericForeignKey below
    place_type = models.ForeignKey(ContentType)
    place_id = models.PositiveIntegerField(db_index=True)
    
    # References one of the models (State, County) in our Places app
    place = generic.GenericForeignKey(ct_field='place_type',fk_field='place_id')
    
    # To future-proof for things like Census 2010
    source = models.ForeignKey(DataSource,db_index=True)
    
    # Census P1 = Total Population
    # ACS B01003
    total = models.PositiveIntegerField(default=0,db_index=True)
    
    # Census P2 = Urban & Rural Population
    urban = models.PositiveIntegerField(default=0,db_index=True)
    rural = models.PositiveIntegerField(default=0,db_index=True)
    
    # Census P3 = Race
    # ACS C02003
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
    # ACS B01001
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
    
    @property
    def violent_crimes_per100k(self):
        """ Violent Crime rate (per 100,000 residents) """
        if self.place and self.place.population_demographics and self.place.population_demographics.total:
            return self.violent_crime / (self.place.population_demographics.total / 100000.0)
        else:
            return None

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

class SocialCharacteristics(CachedModel):
    objects = CachingManager()
    
    place_type = models.ForeignKey(ContentType)
    place_id = models.PositiveIntegerField(db_index=True)
    place = generic.GenericForeignKey(ct_field='place_type',fk_field='place_id')
    
    source = models.ForeignKey(DataSource,db_index=True)

    # ACS B14001: School Enrollment by level of school for population 3yrs and older
    edu_in_school = models.PositiveIntegerField("Enrolled in school",default=0,db_index=True)
    edu_not_in_school = models.PositiveIntegerField("Not enrolled in school",default=0,db_index=True)
    edu_preschool = models.PositiveIntegerField("Enrolled in preschool",default=0,db_index=True)
    edu_kindergarten = models.PositiveIntegerField("Enrolled in kindergarten",default=0,db_index=True)
    edu_1_4 = models.PositiveIntegerField("Enrolled in grade 1 to grade 4",default=0,db_index=True)
    edu_5_8 = models.PositiveIntegerField("Enrolled in grade 5 to grade 8",default=0,db_index=True)
    edu_9_12 = models.PositiveIntegerField("Enrolled in grade 9 to grade 12",default=0,db_index=True)
    edu_undergrad = models.PositiveIntegerField("Enrolled in college (undergraduate)",default=0,db_index=True)
    edu_postgrad = models.PositiveIntegerField("Enrolled in graduate or professional school",default=0,db_index=True)
    
    # ACS B05001 Citizenship
    citizen_born_us = models.PositiveIntegerField("U.S. citizen, born in U.S.",default=0,db_index=True)
    citizen_born_us_err = models.PositiveIntegerField("(margin of error)",default=0,db_index=True)
    citizen_born_pr = models.PositiveIntegerField("U.S. citizen, born in Puerto Rico or U.S. Island Areas",default=0,db_index=True)
    citizen_born_pr_err = models.PositiveIntegerField("(margin of error)",default=0,db_index=True)
    citizen_by_parents = models.PositiveIntegerField("U.S. citizen, born abroad to American parent(s)",default=0,db_index=True)
    citizen_by_parents_err = models.PositiveIntegerField("(margin of error)",default=0,db_index=True)
    citizen_by_naturalization = models.PositiveIntegerField("U.S. citizen by naturalization",default=0,db_index=True)
    citizen_by_naturalization_err = models.PositiveIntegerField("(margin of error)",default=0,db_index=True)
    non_citizen = models.PositiveIntegerField("Not a U.S. citizen",default=0,db_index=True)
    non_citizen_err = models.PositiveIntegerField("(margin of error)",default=0,db_index=True)

    # B19301 Per Capita Income (A-I for race-specific tables)
    per_capita_income = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_white = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_white_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_black = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_black_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_amerindian = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_amerindian_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_asian = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_asian_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_pacislander = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_pacislander_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_other = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_other_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_mixed = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True) # 2 or more races
    per_capita_income_mixed_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True) # 2 or more races
    per_capita_income_white_non_hispanic = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_white_non_hispanic_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_hispanic = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    per_capita_income_hispanic_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)

    # B19313 Aggregate Income (A-I for race-specific tables)
    agg_income = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_white = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_white_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_black = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_black_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_amerindian = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_amerindian_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_asian = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_asian_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_pacislander = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_pacislander_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_other = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_other_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_mixed = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True) # 2 or more races
    agg_income_mixed_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True) # 2 or more races
    agg_income_white_non_hispanic = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_white_non_hispanic_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_hispanic = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    agg_income_hispanic_err = models.DecimalField("(margin of error)",default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)

    # B20002 Median earnings By sex by work experience
    median_income = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    median_income_male = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)
    median_income_female = models.DecimalField(default=Decimal("0"), max_digits=18, decimal_places=2, db_index=True)

    # C20001 Sex by Earnings for population 16+
    earnings_male_0_2499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_2500_4999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_5000_7499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_7500_9999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_10000_12499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_12500_14999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_15000_17499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_17500_19999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_20000_22499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_22500_24999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_25000_29999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_30000_34999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_35000_39999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_40000_44999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_45000_49999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_50000_54999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_50000_64999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_65000_74999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_75000_99999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_male_100000 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_0_2499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_2500_4999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_5000_7499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_7500_9999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_10000_12499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_12500_14999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_15000_17499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_17500_19999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_20000_22499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_22500_24999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_25000_29999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_30000_34999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_35000_39999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_40000_44999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_45000_49999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_50000_54999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_50000_64999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_65000_74999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_75000_99999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_female_100000 = models.PositiveIntegerField(default=0,db_index=True)
    # derived from above
    earnings_0_2499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_2500_4999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_5000_7499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_7500_9999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_10000_12499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_12500_14999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_15000_17499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_17500_19999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_20000_22499 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_22500_24999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_25000_29999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_30000_34999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_35000_39999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_40000_44999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_45000_49999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_50000_54999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_50000_64999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_65000_74999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_75000_99999 = models.PositiveIntegerField(default=0,db_index=True)
    earnings_100000 = models.PositiveIntegerField(default=0,db_index=True)
    
    class Meta:
        verbose_name = "social characteristic data"
        verbose_name_plural = "social characteristic data"
        ordering = ('place_type','place_id')
        unique_together = (('place_type','place_id','source'),)
        db_table = "demographics_soceco"
	
    def __unicode__(self):
        return u"%s social characteristic data" % (self.place)
    __unicode__ = cached_clsmethod(__unicode__, 604800)
