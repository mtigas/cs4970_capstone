from django.core.management.base import NoArgsCommand

from nationbrowse.demographics.models import DataSource,PlacePopulation,CrimeData
from django.contrib.contenttypes.models import ContentType

from string import ascii_uppercase
from django.core import serializers
import os
import gc
import bz2

def create_export(filename,qs):
    s = serializers.get_serializer("xml")()
    f = bz2.BZ2File(filename+".bz2",'w')
    s.serialize(qs.iterator(), ensure_ascii=False, stream=f, indent=2)
    f.close()
    gc.collect()

def split_export(base_filename,qs,split_into):
    num_objs = qs.count()
    per_set = int(num_objs/split_into)
    for i in range(0,split_into):
        start = per_set*i
        if i == split_into-1:
            end = num_objs
        else:
            end = per_set*(i+1)
        print "  %02d/%02d (%d to %d out of %d)..."%(i+1, split_into, start, end, num_objs)
        create_export(base_filename%ascii_uppercase[i],qs[start:end])

class Command(NoArgsCommand):
    help = "Creates fixtures for important Demographics tables."

    def handle_noargs(self, **options):
        nation_type = ContentType.objects.get(app_label="places",model="nation")
        state_type = ContentType.objects.get(app_label="places",model="state")
        county_type = ContentType.objects.get(app_label="places",model="county")
        
        print "Saving Datasources..."
        create_export("/Users/mtigas/Desktop/fixtures/04-datasource.xml",DataSource.objects.all())
        
        print "Saving National demographics..."
        create_export("/Users/mtigas/Desktop/fixtures/05-nation-demographics.xml",PlacePopulation.objects.filter(place_type=nation_type))
        print "Saving National crime data..."
        create_export("/Users/mtigas/Desktop/fixtures/06-nation-crime.xml",CrimeData.objects.filter(place_type=nation_type))
        
        print "Saving State demographics..."
        create_export("/Users/mtigas/Desktop/fixtures/07-state-demographics.xml",PlacePopulation.objects.filter(place_type=state_type))
        print "Saving State crime data..."
        create_export("/Users/mtigas/Desktop/fixtures/08-state-crime.xml",CrimeData.objects.filter(place_type=state_type))
        
        print "Saving County demographics..."
        create_export("/Users/mtigas/Desktop/fixtures/09-county-demographics.xml",PlacePopulation.objects.filter(place_type=county_type))
        print "Saving County crime data..."
        create_export("/Users/mtigas/Desktop/fixtures/10-county-crime.xml",CrimeData.objects.filter(place_type=county_type))
