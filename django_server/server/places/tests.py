# coding=utf-8
"""
Unit tests for Places.
"""

from django.test import TestCase

# Make HTTP requests inside tests never time out.
import socket
socket.setdefaulttimeout(1000)

class PlacesTest(TestCase):
    def test_dummy(self):
        """
        TODO
        """
        self.assert_(True)

"""
from places.models import ZipCode,County
from django.contrib.gis.geos import fromstr
County.objects.get(poly__contains=fromstr("POINT(-73.9706039428711 40.67399850415069)")) # Brooklyn
ZipCode.objects.get(poly__contains=fromstr("POINT(-90.31285285949707 38.83549569788695)")) # Florissant, MO (63031)
ZipCode.objects.get(poly__contains=fromstr("POINT(-90.31688690185547 38.83395795227738)")) # Florissant, MO (63034)
County.objects.get(poly__contains=fromstr("POINT(-90.31688690185547 38.83395795227738)")) # Florissant, MO
County.objects.get(poly__contains=fromstr("POINT(-90.19318073987961 38.622497220401)")) # Downtown STL is NOT in STL County
ZipCode.objects.get(poly__contains=fromstr("POINT(-92.32644081115723 38.94257131896985)")) # MU Campus
ZipCode.objects.get(name="99201").county # Spokane, WA
ZipCode.objects.get(name="65201").counties # 65201 resides in Boone & Callaway
ZipCode.objects.get(name="65201").county
ZipCode.objects.get(name="03579").states # known to be in NH & ME
County.objects.get(name="Boone",state__abbr="MO").zipcodes

# See number of queries & time to see if cache is working
from django.db import connection
print("%s queries:" % len(connection.queries))
time = 0.00
for q in connection.queries:
    print "\t%s" % (q['time'])
    time += float(q['time'])

print("%s queries, %s sec" % (len(connection.queries), time))
"""