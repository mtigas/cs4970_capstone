from django.core.management.base import NoArgsCommand

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from nationbrowse.demographics.models import DataSource,CrimeData
from nationbrowse.places.models import State, County
import csv
import os
from traceback import print_exc
from datetime import date

class Command(NoArgsCommand):
    help = "Disabled. Used for converting Census output data into our PlacePopulation table."

    output_transaction = True
    
    def handle_noargs(self, **options):
        datasource, created = DataSource.objects.get_or_create(
            source="FBI Uniform Crime Reporting Program",
            date = date(2008,01,01),
            defaults = {
                'url' : "http://www.fbi.gov/ucr/cius2008/index.html"
            }
        )
        if created:
            datasource.save()

        data1 = os.path.join(settings.DJANGO_SERVER_DIR, 'server', 'nationbrowse', 'demographics', 'csv_in', '08tbl10.csv')
        f = open(data1)
        csv_reader = csv.reader(f, delimiter=',',quotechar='"')

        fields = csv_reader.next()
        
        county_type = ContentType.objects.get_for_model(County)

        for row in csv_reader:
            try:
                if row[0]:
                    state = State.objects.get(name__iexact=row[0])
            except Exception as e:
                print "%s (%s)" % (row[0], e)
    
    
            county_name = row[1]
            if county_name[-1].isdigit():
                county_name = county_name[:-1]
    
            try:
                county = County.objects.get(state=state,name__iexact=county_name)
            except Exception as e:
                print "%s - %s (%s)" % (state, county_name, e)
            
            try:
                d, created = CrimeData.objects.get_or_create(
                    place_type = county_type,
                    place_id = county.pk,
                    source = datasource
                )
                d.violent_crime = csvstr_to_int(row[2])
                d.murder = csvstr_to_int(row[3])
                d.rape = csvstr_to_int(row[4])
                d.robbery = csvstr_to_int(row[5])
                d.assault = csvstr_to_int(row[6])
    
                d.property_crime = csvstr_to_int(row[7])
                d.burglary = csvstr_to_int(row[8])
                d.larceny_theft = csvstr_to_int(row[9])
                d.auto_theft = csvstr_to_int(row[10])
                d.save()
            except:
                print_exc()

def csvstr_to_int(csvstr):
    s = csvstr.replace(',','')
    if s:
        return int(s)
    else:
        return 0
    