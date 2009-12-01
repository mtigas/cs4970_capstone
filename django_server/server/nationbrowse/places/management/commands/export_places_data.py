from django.core.management.base import NoArgsCommand

from nationbrowse.places.models import Nation,State,County
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
    help = "Creates fixtures for important Places tables."
    
    def handle_noargs(self, **options):
        print "Saving Nation..."
        create_export("/Users/mtigas/Desktop/fixtures/01-nation.xml",Nation.pobjects.all())
        print "Saving States..."
        create_export("/Users/mtigas/Desktop/fixtures/02-state.xml",State.pobjects.all())
        print "Saving Counties..."
        split_export("/Users/mtigas/Desktop/fixtures/03-county-%s.xml",County.pobjects.all(),3)
