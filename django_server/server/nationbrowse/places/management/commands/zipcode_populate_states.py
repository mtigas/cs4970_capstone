from django.core.management.base import NoArgsCommand

from nationbrowse.places.models import State,ZipCode
from multiprocessing import Process
from django.db import IntegrityError, connection, transaction
import gc

def convert_block(qs):
    try:
        connection.close()
    except:
        pass
    
    for z in qs.iterator():
        if not z.poly:
            print "\t%s HAS NO POLY" % z.id
        else:
            # Get an "exact" match: State completely contains the ZipCode polygon
            try:
                z.state = State.objects.only('id','name').get(poly__contains=z.poly)
            except State.DoesNotExist:
                z.state = None
    
            # Get an inexact match: State contains the center of the ZipCode polygon
            if z.state == None:
                try:
                    z.state = State.objects.only('id','name').get(poly__contains=z.center)
                except State.DoesNotExist:
                    z.state = None

            if z.state:
                try:
                    sid = transaction.savepoint()
                    z.save()
                    transaction.savepoint_commit(sid)
                    #print "\t%s: %s" % (z.id, z.state)
                except IntegrityError:
                    transaction.savepoint_rollback(sid)
                    print "\t%s: DB IntegrityError!" % z.id
            else:
                print "\t%s: No primary state" % z.id

def convert_by_block(qs,split_into):
    num_objs = qs.count()
    per_set = int(num_objs/split_into)
    for i in range(0,split_into):
        start = per_set*i
        if i == split_into-1:
            end = num_objs
        else:
            end = per_set*(i+1)
        print "  %02d/%02d (%d to %d out of %d)..."%(i+1, split_into, start, end, num_objs)

        p = Process(
            target=convert_block,
            args=(qs[start:end],)
        )
        p.daemon = False
        p.start()
        p.join()
    
        gc.collect()

class Command(NoArgsCommand):
    help = "Disabled. Used for converting ZipCode shapefile data into the Places data model."
    
    output_transaction = True
    
    def handle_noargs(self, **options):
        convert_by_block(ZipCode.objects.only('id'), 300)

