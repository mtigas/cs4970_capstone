from django.core.management.base import NoArgsCommand

from places.models import State,County,ZipCode
from string import ascii_uppercase
from django.core import serializers
import os
import gc
import bz2

def create_export(filename,model_qs_or_iterator):
    s = serializers.get_serializer("xml")()
    f = bz2.BZ2File(filename+".bz2",'w')
    s.serialize(model_qs_or_iterator, ensure_ascii=False, stream=f, encoding="utf8", indent=4)
    f.close()
    gc.collect()

class Command(NoArgsCommand):
    help = "Creates fixtures for important Places tables."

    def handle_noargs(self, **options):
        create_export("1-state.xml",State.pobjects.iterator())
        create_export("2-county.xml",County.pobjects.iterator())
        gc.collect()
        
        qs = ZipCode.pobjects.all()
        split_into = 6
        num_objs = qs.count()
        per_set = int(num_objs/split_into)
        for i in range(0,split_into):
            print "  %02d/%02d..."%(i+1, split_into)
            start = per_set*i
            if i == split_into-1:
                end = num_objs
            else:
                end = per_set*(i+1)
            create_export("3-zipcode-%s.xml"%ascii_uppercase[i],qs[start:end].iterator())
            gc.collect()
