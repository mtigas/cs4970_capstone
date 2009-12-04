from django.core.management.base import NoArgsCommand

from django.conf import settings
from nationbrowse.demographics.models import DataSource,PlacePopulation,SocialCharacteristics
from nationbrowse.places.models import Nation, State, County
from django.contrib.contenttypes.models import ContentType
import csv
import os
from traceback import print_exc
from datetime import date
from decimal import Decimal

def acs_import_location(place_obj, place_ctype, datasource_obj, data_row1, data_row2):
    d, temp1 = PlacePopulation.objects.get_or_create(
        place_type = place_ctype,
        place_id = place_obj.pk,
        source = datasource_obj,
        defaults = {
            'urban': 0,
            'rural': 0,
            'num_households': 0,
            'pop_in_households': 0,
            'avg_household_size': 0,
            'num_families': 0,
            'pop_in_families': 0,
            'avg_family_size': 0
        }
    )
    c, temp2 = SocialCharacteristics.objects.get_or_create(
        place_type = place_ctype,
        place_id = place_obj.pk,
        source = datasource_obj
    )
    
    d.total = csvstr_to_int(data_row1[4])
    
    d.male = csvstr_to_int(data_row1[6])
    d.male_0_4 = csvstr_to_int(data_row1[8])
    d.male_5_9 = csvstr_to_int(data_row1[10])
    d.male_10_14 = csvstr_to_int(data_row1[12])
    d.male_15_17 = csvstr_to_int(data_row1[14])
    d.male_18_19 = csvstr_to_int(data_row1[16])
    d.male_20 = csvstr_to_int(data_row1[18])
    d.male_21 = csvstr_to_int(data_row1[20])
    d.male_22_24 = csvstr_to_int(data_row1[22])
    d.male_25_29 = csvstr_to_int(data_row1[24])
    d.male_30_34 = csvstr_to_int(data_row1[26])
    d.male_35_39 = csvstr_to_int(data_row1[28])
    d.male_40_44 = csvstr_to_int(data_row1[30])
    d.male_45_49 = csvstr_to_int(data_row1[32])
    d.male_50_54 = csvstr_to_int(data_row1[34])
    d.male_55_59 = csvstr_to_int(data_row1[36])
    d.male_60_61 = csvstr_to_int(data_row1[38])
    d.male_62_64 = csvstr_to_int(data_row1[40])
    d.male_65_66 = csvstr_to_int(data_row1[42])
    d.male_67_69 = csvstr_to_int(data_row1[44])
    d.male_70_74 = csvstr_to_int(data_row1[46])
    d.male_75_79 = csvstr_to_int(data_row1[48])
    d.male_80_84 = csvstr_to_int(data_row1[50])
    d.male_85_plus = csvstr_to_int(data_row1[52])
    
    d.female = csvstr_to_int(data_row1[54])
    d.female_0_4 = csvstr_to_int(data_row1[56])
    d.female_5_9 = csvstr_to_int(data_row1[58])
    d.female_10_14 = csvstr_to_int(data_row1[60])
    d.female_15_17 = csvstr_to_int(data_row1[62])
    d.female_18_19 = csvstr_to_int(data_row1[64])
    d.female_20 = csvstr_to_int(data_row1[66])
    d.female_21 = csvstr_to_int(data_row1[68])
    d.female_22_24 = csvstr_to_int(data_row1[70])
    d.female_25_29 = csvstr_to_int(data_row1[72])
    d.female_30_34 = csvstr_to_int(data_row1[74])
    d.female_35_39 = csvstr_to_int(data_row1[76])
    d.female_40_44 = csvstr_to_int(data_row1[78])
    d.female_45_49 = csvstr_to_int(data_row1[80])
    d.female_50_54 = csvstr_to_int(data_row1[82])
    d.female_55_59 = csvstr_to_int(data_row1[84])
    d.female_60_61 = csvstr_to_int(data_row1[86])
    d.female_62_64 = csvstr_to_int(data_row1[88])
    d.female_65_66 = csvstr_to_int(data_row1[90])
    d.female_67_69 = csvstr_to_int(data_row1[92])
    d.female_70_74 = csvstr_to_int(data_row1[94])
    d.female_75_79 = csvstr_to_int(data_row1[96])
    d.female_80_84 = csvstr_to_int(data_row1[98])
    d.female_85_plus = csvstr_to_int(data_row1[100])
    
    d.age_0_4 = csvstr_to_int(data_row1[56]) + csvstr_to_int(data_row1[56-48])
    d.age_5_9 = csvstr_to_int(data_row1[58]) + csvstr_to_int(data_row1[58-48])
    d.age_10_14 = csvstr_to_int(data_row1[60]) + csvstr_to_int(data_row1[60-48])
    d.age_15_17 = csvstr_to_int(data_row1[62]) + csvstr_to_int(data_row1[62-48])
    d.age_18_19 = csvstr_to_int(data_row1[64]) + csvstr_to_int(data_row1[64-48])
    d.age_20 = csvstr_to_int(data_row1[66]) + csvstr_to_int(data_row1[66-48])
    d.age_21 = csvstr_to_int(data_row1[68]) + csvstr_to_int(data_row1[68-48])
    d.age_22_24 = csvstr_to_int(data_row1[70]) + csvstr_to_int(data_row1[70-48])
    d.age_25_29 = csvstr_to_int(data_row1[72]) + csvstr_to_int(data_row1[72-48])
    d.age_30_34 = csvstr_to_int(data_row1[74]) + csvstr_to_int(data_row1[74-48])
    d.age_35_39 = csvstr_to_int(data_row1[76]) + csvstr_to_int(data_row1[76-48])
    d.age_40_44 = csvstr_to_int(data_row1[78]) + csvstr_to_int(data_row1[78-48])
    d.age_45_49 = csvstr_to_int(data_row1[80]) + csvstr_to_int(data_row1[80-48])
    d.age_50_54 = csvstr_to_int(data_row1[82]) + csvstr_to_int(data_row1[82-48])
    d.age_55_59 = csvstr_to_int(data_row1[84]) + csvstr_to_int(data_row1[84-48])
    d.age_60_61 = csvstr_to_int(data_row1[86]) + csvstr_to_int(data_row1[86-48])
    d.age_62_64 = csvstr_to_int(data_row1[88]) + csvstr_to_int(data_row1[88-48])
    d.age_65_66 = csvstr_to_int(data_row1[90]) + csvstr_to_int(data_row1[90-48])
    d.age_67_69 = csvstr_to_int(data_row1[92]) + csvstr_to_int(data_row1[92-48])
    d.age_70_74 = csvstr_to_int(data_row1[94]) + csvstr_to_int(data_row1[94-48])
    d.age_75_79 = csvstr_to_int(data_row1[96]) + csvstr_to_int(data_row1[96-48])
    d.age_80_84 = csvstr_to_int(data_row1[98]) + csvstr_to_int(data_row1[98-48])
    d.age_85_plus = csvstr_to_int(data_row1[100]) + csvstr_to_int(data_row1[100-48])
    
    d.onerace = csvstr_to_int(data_row1[106])
    d.onerace_white = csvstr_to_int(data_row1[108])
    d.onerace_black = csvstr_to_int(data_row1[110])
    d.onerace_amerindian = csvstr_to_int(data_row1[112])
    d.onerace_asian = csvstr_to_int(data_row1[114])
    d.onerace_pacislander = csvstr_to_int(data_row1[116])
    d.onerace_other = csvstr_to_int(data_row1[118])
    d.tworace = csvstr_to_int(data_row1[126])
    d.threerace = csvstr_to_int(data_row1[138])
    
    c.citizen_born_us = csvstr_to_int(data_row1[144])
    c.citizen_born_us_err = csvstr_to_int(data_row1[145])
    c.citizen_born_pr = csvstr_to_int(data_row1[146])
    c.citizen_born_pr_err = csvstr_to_int(data_row1[147])
    c.citizen_by_parents = csvstr_to_int(data_row1[148])
    c.citizen_by_parents_err = csvstr_to_int(data_row1[149])
    c.citizen_by_naturalization = csvstr_to_int(data_row1[150])
    c.citizen_by_naturalization_err = csvstr_to_int(data_row1[151])
    c.non_citizen = csvstr_to_int(data_row1[152])
    c.non_citizen_err = csvstr_to_int(data_row1[153])
    
    c.edu_in_school = csvstr_to_int(data_row1[156])
    c.edu_not_in_school = csvstr_to_int(data_row1[172])
    c.edu_preschool = csvstr_to_int(data_row1[158])
    c.edu_kindergarten = csvstr_to_int(data_row1[160])
    c.edu_1_4 = csvstr_to_int(data_row1[162])
    c.edu_5_8 = csvstr_to_int(data_row1[164])
    c.edu_9_12 = csvstr_to_int(data_row1[166])
    c.edu_undergrad = csvstr_to_int(data_row1[168])
    c.edu_postgrad = csvstr_to_int(data_row1[170])
    
    c.per_capita_income = csvstr_to_float(data_row1[174])
    c.per_capita_income_err = csvstr_to_float(data_row1[175])
    c.per_capita_income_white = csvstr_to_float(data_row1[176])
    c.per_capita_income_white_err = csvstr_to_float(data_row1[177])
    c.per_capita_income_black = csvstr_to_float(data_row1[178])
    c.per_capita_income_black_err = csvstr_to_float(data_row1[179])
    c.per_capita_income_amerindian = csvstr_to_float(data_row1[180])
    c.per_capita_income_amerindian_err = csvstr_to_float(data_row1[181])
    c.per_capita_income_asian = csvstr_to_float(data_row1[182])
    c.per_capita_income_asian_err = csvstr_to_float(data_row1[183])
    c.per_capita_income_pacislander = csvstr_to_float(data_row1[184])
    c.per_capita_income_pacislander_err = csvstr_to_float(data_row1[185])
    c.per_capita_income_other = csvstr_to_float(data_row1[186])
    c.per_capita_income_other_err = csvstr_to_float(data_row1[187])
    c.per_capita_income_mixed = csvstr_to_float(data_row1[188]) # 2 or more races
    c.per_capita_income_mixed_err = csvstr_to_float(data_row1[189]) # 2 or more races
    c.per_capita_income_white_non_hispanic = csvstr_to_float(data_row1[190])
    c.per_capita_income_white_non_hispanic_err = csvstr_to_float(data_row1[191])
    c.per_capita_income_hispanic = csvstr_to_float(data_row1[192])
    c.per_capita_income_hispanic_err = csvstr_to_float(data_row1[193])
    
    c.agg_income = csvstr_to_float(data_row1[194])
    c.agg_income_err = csvstr_to_float(data_row1[195])
    c.agg_income_white = csvstr_to_float(data_row1[196])
    c.agg_income_white_err = csvstr_to_float(data_row1[197])
    c.agg_income_black = csvstr_to_float(data_row1[198])
    c.agg_income_black_err = csvstr_to_float(data_row1[199])
    c.agg_income_amerindian = csvstr_to_float(data_row1[200])
    c.agg_income_amerindian_err = csvstr_to_float(data_row1[201])
    c.agg_income_asian = csvstr_to_float(data_row1[202])
    c.agg_income_asian_err = csvstr_to_float(data_row1[203])
    c.agg_income_pacislander = csvstr_to_float(data_row1[204])
    c.agg_income_pacislander_err = csvstr_to_float(data_row1[205])
    c.agg_income_other = csvstr_to_float(data_row1[206])
    c.agg_income_other_err = csvstr_to_float(data_row1[207])
    c.agg_income_mixed = csvstr_to_float(data_row1[208]) # 2 or more races
    c.agg_income_mixed_err = csvstr_to_float(data_row1[209]) # 2 or more races
    c.agg_income_white_non_hispanic = csvstr_to_float(data_row1[210])
    c.agg_income_white_non_hispanic_err = csvstr_to_float(data_row1[211])
    c.agg_income_hispanic = csvstr_to_float(data_row1[212])
    c.agg_income_hispanic_err = csvstr_to_float(data_row1[213])
    
    c.earnings_male_0_2499 = csvstr_to_int(data_row1[218])
    c.earnings_male_2500_4999 = csvstr_to_int(data_row1[220])
    c.earnings_male_5000_7499 = csvstr_to_int(data_row1[222])
    c.earnings_male_7500_9999 = csvstr_to_int(data_row1[224])
    c.earnings_male_10000_12499 = csvstr_to_int(data_row1[226])
    c.earnings_male_12500_14999 = csvstr_to_int(data_row1[228])
    c.earnings_male_15000_17499 = csvstr_to_int(data_row1[230])
    c.earnings_male_17500_19999 = csvstr_to_int(data_row1[232])
    c.earnings_male_20000_22499 = csvstr_to_int(data_row1[234])
    c.earnings_male_22500_24999 = csvstr_to_int(data_row1[236])
    c.earnings_male_25000_29999 = csvstr_to_int(data_row1[238])
    c.earnings_male_30000_34999 = csvstr_to_int(data_row1[240])
    c.earnings_male_35000_39999 = csvstr_to_int(data_row1[242])
    c.earnings_male_40000_44999 = csvstr_to_int(data_row1[244])
    c.earnings_male_45000_49999 = csvstr_to_int(data_row1[246])
    c.earnings_male_50000_54999 = csvstr_to_int(data_row1[248])
    c.earnings_male_50000_64999 = csvstr_to_int(data_row1[250])
    c.earnings_male_65000_74999 = csvstr_to_int(data_row1[252])
    c.earnings_male_75000_99999 = csvstr_to_int(data_row2[4])
    c.earnings_male_100000 = csvstr_to_int(data_row2[6])
    
    c.earnings_female_0_2499 = csvstr_to_int(data_row2[10])
    c.earnings_female_2500_4999 = csvstr_to_int(data_row2[12])
    c.earnings_female_5000_7499 = csvstr_to_int(data_row2[14])
    c.earnings_female_7500_9999 = csvstr_to_int(data_row2[16])
    c.earnings_female_10000_12499 = csvstr_to_int(data_row2[18])
    c.earnings_female_12500_14999 = csvstr_to_int(data_row2[20])
    c.earnings_female_15000_17499 = csvstr_to_int(data_row2[22])
    c.earnings_female_17500_19999 = csvstr_to_int(data_row2[24])
    c.earnings_female_20000_22499 = csvstr_to_int(data_row2[26])
    c.earnings_female_22500_24999 = csvstr_to_int(data_row2[28])
    c.earnings_female_25000_29999 = csvstr_to_int(data_row2[30])
    c.earnings_female_30000_34999 = csvstr_to_int(data_row2[32])
    c.earnings_female_35000_39999 = csvstr_to_int(data_row2[34])
    c.earnings_female_40000_44999 = csvstr_to_int(data_row2[36])
    c.earnings_female_45000_49999 = csvstr_to_int(data_row2[38])
    c.earnings_female_50000_54999 = csvstr_to_int(data_row2[40])
    c.earnings_female_50000_64999 = csvstr_to_int(data_row2[42])
    c.earnings_female_65000_74999 = csvstr_to_int(data_row2[44])
    c.earnings_female_75000_99999 = csvstr_to_int(data_row2[46])
    c.earnings_female_100000 = csvstr_to_int(data_row2[48])
    
    c.earnings_0_2499 = csvstr_to_int(data_row1[218]) + csvstr_to_int(data_row2[10])
    c.earnings_2500_4999 = csvstr_to_int(data_row1[220]) + csvstr_to_int(data_row2[12])
    c.earnings_5000_7499 = csvstr_to_int(data_row1[222]) + csvstr_to_int(data_row2[14])
    c.earnings_7500_9999 = csvstr_to_int(data_row1[224]) + csvstr_to_int(data_row2[16])
    c.earnings_10000_12499 = csvstr_to_int(data_row1[226]) + csvstr_to_int(data_row2[18])
    c.earnings_12500_14999 = csvstr_to_int(data_row1[228]) + csvstr_to_int(data_row2[20])
    c.earnings_15000_17499 = csvstr_to_int(data_row1[230]) + csvstr_to_int(data_row2[22])
    c.earnings_17500_19999 = csvstr_to_int(data_row1[232]) + csvstr_to_int(data_row2[24])
    c.earnings_20000_22499 = csvstr_to_int(data_row1[234]) + csvstr_to_int(data_row2[26])
    c.earnings_22500_24999 = csvstr_to_int(data_row1[236]) + csvstr_to_int(data_row2[28])
    c.earnings_25000_29999 = csvstr_to_int(data_row1[238]) + csvstr_to_int(data_row2[30])
    c.earnings_30000_34999 = csvstr_to_int(data_row1[240]) + csvstr_to_int(data_row2[32])
    c.earnings_35000_39999 = csvstr_to_int(data_row1[242]) + csvstr_to_int(data_row2[34])
    c.earnings_40000_44999 = csvstr_to_int(data_row1[244]) + csvstr_to_int(data_row2[36])
    c.earnings_45000_49999 = csvstr_to_int(data_row1[246]) + csvstr_to_int(data_row2[38])
    c.earnings_50000_54999 = csvstr_to_int(data_row1[248]) + csvstr_to_int(data_row2[40])
    c.earnings_50000_64999 = csvstr_to_int(data_row1[250]) + csvstr_to_int(data_row2[42])
    c.earnings_65000_74999 = csvstr_to_int(data_row1[252]) + csvstr_to_int(data_row2[44])
    c.earnings_75000_99999 = csvstr_to_int(data_row2[4]) + csvstr_to_int(data_row2[46])
    c.earnings_100000 = csvstr_to_int(data_row2[6]) + csvstr_to_int(data_row2[48])
    
    c.median_income = csvstr_to_float(data_row2[50])
    c.median_income_male = csvstr_to_float(data_row2[52])
    c.median_income_female = csvstr_to_float(data_row2[54])
    
    d.save()
    c.save()
    
def acs_import(model_name, datasource):
    data1 = os.path.join(settings.DJANGO_SERVER_DIR, 'server', 'nationbrowse', 'demographics', 'csv_in', 'acs_08', '%s_a.txt' % model_name)
    data2 = os.path.join(settings.DJANGO_SERVER_DIR, 'server', 'nationbrowse', 'demographics', 'csv_in', 'acs_08', '%s_a.txt' % model_name)
    content_type = ContentType.objects.get(app_label="places",model=model_name)
    
    f_a = open(data1)
    f_b= open(data2)
    csv_reader_a = csv.reader(f_a, delimiter='|')
    csv_reader_b =  csv.reader(f_b, delimiter='|')

    # Skip the headers (but grab a copy of them)
    header_a1 = csv_reader_a.next()
    header_a2 = csv_reader_a.next()
    header_b1 = csv_reader_b.next()
    header_b2 = csv_reader_b.next()
    headers_a = zip(header_a1,header_a2)
    headers_b = zip(header_b1,header_b2)

    for row_a in csv_reader_a:
        row_b = csv_reader_b.next()

        if model_name is "nation":
            place = Nation.objects.get(id=1)
        elif model_name is "state":
            place = State.objects.get(fips_code=int(row_a[1]))
        elif model_name is "county":
            state_fips = int(row_a[1][:2])
            county_fips = int(row_a[1][2:])
            place = County.objects.get(state__fips_code=state_fips, fips_code=county_fips)
        else:
            place = None
        
        if place:
            print place
            print row_a[3]
        else:
            print "COULD NOT GET PLACE"
            print "FIPS %s: %s" % (row_a[1], row_a[3])
            raise Exception
        print
        
        acs_import_location(place, content_type, datasource, row_a, row_b)

class Command(NoArgsCommand):
    help = ""

    output_transaction = True
    
    def handle_noargs(self, **options):
        datasource = DataSource.objects.get(id=3)
        acs_import("nation", datasource)
        acs_import("state", datasource)
        acs_import("county", datasource)
        """
        try:
            state = State.objects.get(name__iexact=row[0])
        except Exception as e:
            print "%s (%s)" % (row[0], e)

        try:
            d, created = CrimeData.objects.get_or_create(
                place_type = state_type,
                place_id = state.pk,
                source = datasource
            )
            d.violent_crime = csvstr_to_int(row[1])
            d.murder = csvstr_to_int(row[2])
            d.rape = csvstr_to_int(row[3])
            d.robbery = csvstr_to_int(row[4])
            d.assault = csvstr_to_int(row[5])

            d.property_crime = csvstr_to_int(row[6])
            d.burglary = csvstr_to_int(row[7])
            d.larceny_theft = csvstr_to_int(row[8])
            d.auto_theft = csvstr_to_int(row[9])
            d.save()
        except:
            print_exc()
        """

def csvstr_to_int(csvstr):
    s = csvstr.replace(',','')
    if s:
        return int(s)
    else:
        return 0

def csvstr_to_float(csvstr):
    s = csvstr.replace(',','')
    if s:
        return Decimal("%10.4f" % float(s))
    else:
        return Decimal("0")
