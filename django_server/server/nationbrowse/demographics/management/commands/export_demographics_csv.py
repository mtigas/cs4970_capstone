from django.core.management.base import NoArgsCommand

from nationbrowse.places.models import State,County
import csv

def create_export(filename, qs):
    """
    qs should be a queryset or iterator of PolyModel-ish objects
    """
    fields = ["place_id",
        "total","urban","rural",
        "onerace", "onerace_white", "onerace_black", "onerace_amerindian", "onerace_asian", "onerace_pacislander", "onerace_other",
        "tworace", "threerace", "fourrace", "fiverace", "sixrace",
        "white","black","amerindian","asian","pacislander","other",
        "male", "male_0_4", "male_5_9", "male_10_14", "male_15_17", "male_18_19", "male_20", "male_21", "male_22_24", "male_25_29", "male_30_34", "male_35_39", "male_40_44", "male_45_49", "male_50_54", "male_55_59", "male_60_61", "male_62_64", "male_65_66", "male_67_69", "male_70_74", "male_75_79", "male_80_84", "male_85_plus",
        "female", "female_0_4", "female_5_9", "female_10_14", "female_15_17", "female_18_19", "female_20", "female_21", "female_22_24", "female_25_29", "female_30_34", "female_35_39", "female_40_44", "female_45_49", "female_50_54", "female_55_59", "female_60_61", "female_62_64", "female_65_66", "female_67_69", "female_70_74", "female_75_79", "female_80_84", "female_85_plus",
        "age_0_4", "age_5_9", "age_10_14", "age_15_17", "age_18_19", "age_20", "age_21", "age_22_24", "age_25_29", "age_30_34", "age_35_39", "age_40_44", "age_45_49", "age_50_54", "age_55_59", "age_60_61", "age_62_64", "age_65_66", "age_67_69", "age_70_74", "age_75_79", "age_80_84", "age_85_plus",
        "num_households", "pop_in_households", "avg_household_size",
        "num_families", "pop_in_families", "avg_family_size"
    ]
    outfile = open(filename,"w")
    writer = csv.writer(outfile)
    
    writer.writerow( ['place_name',] + fields )
    
    for place in qs:
        demographics = place.population_demographics
        if demographics:
            writer.writerow(
                [str(place),] + map(lambda field: getattr(demographics,field), fields)
            )
    
    outfile.close()

class Command(NoArgsCommand):
    help = "Creates fixtures for important Demographics tables."

    def handle_noargs(self, **options):
        print "Saving Demographics to CSV..."
        create_export("/Users/mtigas/Desktop/csv/1-state.csv",State.objects.order_by('name').defer('poly').all().iterator())
        create_export("/Users/mtigas/Desktop/csv/2-county.csv",County.objects.order_by('state__name','name').defer('poly').all().iterator())
        