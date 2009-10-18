from django.core.management.base import NoArgsCommand

from nationbrowse.places.models import State,ZipCode
from django.db import IntegrityError, transaction
from traceback import print_exc
import gc

class Command(NoArgsCommand):
    help = "Disabled. Used for converting ZipCode shapefile data into the Places data model."

    output_transaction = True
    
    def handle_noargs(self, **options):
        gc.enable()
        
        for z in ZipCode.objects.only('id').iterator():
            z.states = State.objects.only('id',).filter(poly__intersects=z.poly).all()
            
            s = z.states.only('id','name').all()
            if z.states.count() == 1:
                z.primary_state = s[0]
            else:
                z.primary_state = None
            
            print "%s: %s" % (z.id, ','.join(map(lambda x:x.name,s)))
            
            try:
                sid = transaction.savepoint()
                z.save()
                transaction.savepoint_commit(sid)
            except IntegrityError:
                transaction.savepoint_rollback(sid)
                print u"\t!!! Error saving ZipCode %s !!!" % (z)
