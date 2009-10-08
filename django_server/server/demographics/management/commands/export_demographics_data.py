from django.core.management.base import NoArgsCommand

from demographics.models import DataSource,PlacePopulation
from django.contrib.contenttypes.models import ContentType

from string import ascii_uppercase
from django.core import serializers
import os
import gc
import bz2

def create_export(filename,model_qs_or_iterator):
    s = serializers.get_serializer("xml")()
    f = bz2.BZ2File(filename+".bz2",'w')
    s.serialize(model_qs_or_iterator, ensure_ascii=False, stream=f, indent=4)
    f.close()
    gc.collect()

class Command(NoArgsCommand):
    help = "Creates fixtures for important Demographics tables."

    def handle_noargs(self, **options):
        state_type = ContentType.objects.get(app_label="places",model="state")
        county_type = ContentType.objects.get(app_label="places",model="county")
        zipcode_type = ContentType.objects.get(app_label="places",model="zipcode")
        
        print "Exporting DataSources and State data..."
        create_export("4-demographics-A_datasources-state.xml",
            list(DataSource.objects.all()) + list(PlacePopulation.objects.filter(place_type=state_type))
        )
        gc.collect()
        
        print "Exporting County data..."
        create_export("4-demographics-B_county.xml",PlacePopulation.objects.filter(place_type=county_type).iterator())
        gc.collect()
        
        print "Exporting ZipCode data..."
        create_export("4-demographics-C_zipcode.xml",PlacePopulation.objects.filter(place_type=zipcode_type).iterator())
        """
        qs = PlacePopulation.objects.filter(place_type=zipcode_type)
        split_into = 4
        num_objs = qs.count()
        per_set = int(num_objs/split_into)
        for i in range(0,split_into):
            print "  %02d/%02d..."%(i+1, split_into)
            start = per_set*i
            if i == split_into-1:
                end = num_objs
            else:
                end = per_set*(i+1)
            create_export("4-demographics-C_zipcode%s.xml"%ascii_uppercase[i],qs[start:end].iterator())
            gc.collect()
        """
