from django.core.management.base import NoArgsCommand

from demographics.models import PlacePopulation
from django.core import serializers
import os
import gc
import codecs
from xml.dom.minidom import parse
import bz2

def create_export(filename,model_qs_or_iterator):
    s = serializers.get_serializer("xml")()
    
    # Dump the "flat" XML
    out = open(filename+".tmp", "w")
    s.serialize(model_qs_or_iterator, ensure_ascii=False, stream=out)
    out.close()
    out = None
    model_qs_or_iterator = None
    gc.collect()
    
    # Open the XML as a UTF-8 string and minidom parse it
    tmp = open(filename+".tmp",'r')
    t = codecs.EncodedFile(tmp,'utf-8')
    dom = parse(t)
    tmp.close()
    tmp = None
    t = None
    gc.collect()
    
    # Write the "pretty" XML out to the target file
    # We're making this a bz2-encoded file since Django
    # can accept these by default when performing "loaddata"
    f = bz2.BZ2File(filename+".bz2",'w')
    f.write(dom.toprettyxml(encoding="utf-8"))
    f.close()
    f = None
    dom = None
    gc.collect()

    # Delete the flat "temp" file.
    os.unlink(filename+".tmp")
    gc.collect()

class Command(NoArgsCommand):
    help = "Creates fixtures for important Demographics tables."

    def handle_noargs(self, **options):
        create_export("4-demographics_stateonly.xml",PlacePopulation.objects.iterator())
        