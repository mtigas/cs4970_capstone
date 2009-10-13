from django.core.management.base import NoArgsCommand

from nationbrowse.demographics.models import PopulationImport,PlacePopulation
from nationbrowse.places.models import County,State
from django.db import IntegrityError, transaction
import gc

class Command(NoArgsCommand):
    help = "Disabled. Used for converting Census output data into our PlacePopulation table."

    output_transaction = True
    
    def handle_noargs(self, **options):
        return True
    
    def XXXhandle_noargs(self, **options):
        gc.enable()
        for p in PopulationImport.objects.iterator():
            try:
                # First two digits are the state FIPS, the last three
                # belong to the county (since County FIPS is only unique
                # within a state)
                state_fips = int(str(p.fips_code)[:-3])
                county_fips = (str(p.fips_code)[-3:])
                
                print "Population Import %s (%s-%s)" % (p.name, state_fips,county_fips)
                state = State.objects.get(fips_code=state_fips)
                county = County.objects.get(state=state,fips_code=county_fips)
                
                print "\tState: %s (%s), County: %s (%s)" % (state, state.fips_code, county, county.fips_code)
                pp = PlacePopulation(
                    place = county,
                    total = p.p001001,
                    urban = p.p002002,
                    rural = p.p002005,

                    onerace = p.p003002,
                    onerace_white = p.p003003,
                    onerace_black = p.p003004,
                    onerace_amerindian = p.p003005,
                    onerace_asian = p.p003006,
                    onerace_pacislander = p.p003007,
                    onerace_other = p.p003008,
                    tworace = p.p003010,
                    threerace = p.p003026,
                    fourrace = p.p003047,
                    fiverace = p.p003063,
                    sixrace = p.p003070,


                    white = p.p009002,
                    black = p.p009003,
                    amerindian = p.p009004,
                    asian = p.p009005,
                    pacislander = p.p009006,
                    other = p.p009007,

                    male = p.p012002,
                    male_0_4 = p.p012003,
                    male_5_9 = p.p012004,
                    male_10_14 = p.p012005,
                    male_15_17 = p.p012006,
                    male_18_19 = p.p012007,
                    male_20 = p.p012008,
                    male_21 = p.p012009,
                    male_22_24 = p.p012010,
                    male_25_29 = p.p012011,
                    male_30_34 = p.p012012,
                    male_35_39 = p.p012013,
                    male_40_44 = p.p012014,
                    male_45_49 = p.p012015,
                    male_50_54 = p.p012016,
                    male_55_59 = p.p012017,
                    male_60_61 = p.p012018,
                    male_62_64 = p.p012019,
                    male_65_66 = p.p012020,
                    male_67_69 = p.p012021,
                    male_70_74 = p.p012022,
                    male_75_79 = p.p012023,
                    male_80_84 = p.p012024,
                    male_85_plus = p.p012025,
                    female = p.p012026,
                    female_0_4 = p.p012027,
                    female_5_9 = p.p012028,
                    female_10_14 = p.p012029,
                    female_15_17 = p.p012030,
                    female_18_19 = p.p012031, 
                    female_20 =  p.p012032,
                    female_21 =  p.p012033,
                    female_22_24 =  p.p012034,
                    female_25_29 = p.p012035,
                    female_30_34 = p.p012036,
                    female_35_39 = p.p012037,
                    female_40_44 = p.p012038,
                    female_45_49 = p.p012039,
                    female_50_54 = p.p012040,
                    female_55_59 = p.p012041,
                    female_60_61 = p.p012042,
                    female_62_64 = p.p012043,
                    female_65_66 = p.p012044,
                    female_67_69 = p.p012045,
                    female_70_74 = p.p012046,
                    female_75_79 = p.p012047,
                    female_80_84 = p.p012048,
                    female_85_plus = p.p012049,

                    age_0_4 = p.p012003+p.p012027,
                    age_5_9 = p.p012004+p.p012028,
                    age_10_14 = p.p012005+p.p012029,
                    age_15_17 = p.p012006+p.p012030,
                    age_18_19 = p.p012007+p.p012031,
                    age_20 = p.p012008+p.p012032,
                    age_21 = p.p012009+p.p012033,
                    age_22_24 = p.p012010+p.p012034,
                    age_25_29 = p.p012011+p.p012035,
                    age_30_34 = p.p012012+p.p012036,
                    age_35_39 = p.p012013+p.p012037,
                    age_40_44 = p.p012014+p.p012038,
                    age_45_49 = p.p012015+p.p012039,
                    age_50_54 = p.p012016+p.p012040,
                    age_55_59 = p.p012017+p.p012041,
                    age_60_61 = p.p012018+p.p012042,
                    age_62_64 = p.p012019+p.p012043,
                    age_65_66 = p.p012020+p.p012044,
                    age_67_69 = p.p012021+p.p012045,
                    age_70_74 = p.p012022+p.p012046,
                    age_75_79 = p.p012023+p.p012047,
                    age_80_84 = p.p012024+p.p012048,
                    age_85_plus = p.p012025+p.p012049,

                    num_households = p.p015001,
                    pop_in_households = p.p016001,
                    avg_household_size = p.p017001,

                    num_families = p.p031001,
                    pop_in_families = p.p032001,
                    avg_family_size =p.p033001
                )
                try:
                    sid = transaction.savepoint()
                    pp.save()
                    transaction.savepoint_commit(sid)
                    print u"\tPlacePopulation %s saved" % (pp.id)
                except IntegrityError:
                    transaction.savepoint_rollback(sid)
                    print u"\t!!! Error saving county population for %s (%s) !!!" % (p.name, p.fips_code)
            except County.DoesNotExist:
                print "\tCounty does not exist"
            gc.collect()
