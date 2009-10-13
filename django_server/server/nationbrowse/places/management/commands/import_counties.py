from django.core.management.base import NoArgsCommand

from nationbrowse.places.models import ConversionCounty,State,County
from django.template.defaultfilters import slugify
from django.db import IntegrityError, connection, transaction
    
class Command(NoArgsCommand):
    help = "Disabled. Used for converting County shapefile data into the Places data model."

    output_transaction = True
    
    def handle_noargs(self, **options):
        return True
    
    def XXXhandle_noargs(self, **options):
        a = ConversionCounty.objects.get(pk=591)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Fairfax City"
        a.namelsad_x = "Fairfax City"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        a = ConversionCounty.objects.get(pk=719)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Fairfax County"
        a.namelsad_x = "Fairfax County"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        a = ConversionCounty.objects.get(pk=1794)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Franklin City"
        a.namelsad_x = "Franklin City"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        a = ConversionCounty.objects.get(pk=1646)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Franklin County"
        a.namelsad_x = "Franklin County"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        a = ConversionCounty.objects.get(pk=582)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Roanoke City"
        a.namelsad_x = "Roanoke City"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        a = ConversionCounty.objects.get(pk=2194)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Roanoke County"
        a.namelsad_x = "Roanoke County"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        a = ConversionCounty.objects.get(pk=1647)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Bedford City"
        a.namelsad_x = "Bedford City"
        a.save()

        a = ConversionCounty.objects.get(pk=3059)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Bedford County"
        a.namelsad_x = "Bedford County"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        a = ConversionCounty.objects.get(pk=3082)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Richmond City"
        a.namelsad_x = "Richmond City"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        a = ConversionCounty.objects.get(pk=3069)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Richmond County"
        a.namelsad_x = "Richmond County"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        a = ConversionCounty.objects.get(pk=3052)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "St. Louis City"
        a.namelsad_x = "St. Louis City"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        a = ConversionCounty.objects.get(pk=2473)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "St. Louis County"
        a.namelsad_x = "St. Louis County"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()


        a = ConversionCounty.objects.get(pk=2815)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Baltimore City"
        a.namelsad_x = "Baltimore City"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        a = ConversionCounty.objects.get(pk=806)
        oname = a.name
        onamelsad = a.namelsad
        a.name_x = "Baltimore County"
        a.namelsad_x = "Baltimore County"
        print "Convert %s: %s (%s) -> %s" % (a.pk, oname, onamelsad, a.name)
        a.save()

        print "\n\n\n"
        
        for c in ConversionCounty.objects.defer('wkb_geometry').all():
            new_c = county_from_conversioncounty(c)
            state = State.objects.get(fips_code=c.statefp)
            try:
                sid = transaction.savepoint()
                new_c.save()
                transaction.savepoint_commit(sid)

                print "County %s saved (%s, %s) / %s" % (c.id, new_c.name, new_c.state, new_c.slug)
            except IntegrityError:
                transaction.savepoint_rollback(sid)
                print u"!!! IntegrityError on ConversionCounty: %s (%s, %s)  !!!" % (c.pk, c.name, state)

def county_from_conversioncounty(c):
    state = State.objects.get(fips_code=c.statefp)
    
    new_c = County()
    new_c.name = c.name
    new_c.long_name = c.namelsad
    new_c.fips_code = c.countyfp
    new_c.state = state
    new_c.csafp = c.csafp
    new_c.cbsafp = c.cbsafp
    new_c.metdivfp = c.metdivfp
    new_c.poly = c.wkb_geometry
    new_c.slug = slugify(u"%s %s" % (c.name, state.slug))
    
    if c.pk == 116:
        new_c.slug = "district-of-columbia"
    
    return new_c
