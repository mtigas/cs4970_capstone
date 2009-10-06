from django.core.management.base import NoArgsCommand

from places.models import ConversionZipCode,State,ZipCode
from django.db import IntegrityError, transaction
import gc

class Command(NoArgsCommand):
    help = "Disabled. Used for converting ZipCode shapefile data into the Places data model."

    output_transaction = True
    
    def handle_noargs(self, **options):
        return True
    
    def XXXhandle_noargs(self, **options):
        gc.enable()
        
        qs = ConversionZipCode.objects.order_by('zipcode_x').defer('wkb_geometry')
        total = qs.count()
        cur = 1
        for z in qs.iterator():
            print "[%s/%s] Converting ZIP code %s ..." % (cur,total,z)
            cur = cur+1
            
            new_z = ZipCode(
                id=int(z.zipcode),
                name=z.zipcode,
                slug=z.zipcode,
                poly=z.wkb_geometry
            )

            try:
                sid = transaction.savepoint()
                new_z.save()
                transaction.savepoint_commit(sid)
            except IntegrityError:
                transaction.savepoint_rollback(sid)
                print u"\t!!! Error saving ZipCode %s !!!" % (z)

            z = None
            new_z = None
            sid = None
            if (cur%500 == 0):
                gc.collect()
