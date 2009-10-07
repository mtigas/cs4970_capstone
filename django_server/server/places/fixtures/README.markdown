# Fixtures!

The fun and easy way to share and load "fixed" data. Fixtures representing State, County, and ZipCode models are bundled in the repository (note that these bundled fixtures do not contain geographic shapefile data).

To use these, make sure you have a database to work with. (The following commands assume you're working in the `server/capstone` directory.) Perform a `syncdb` to make sure Django has all of the tables it needs.

    python manage.py syncdb --noinput

And then run these to load the actual data:

    python manage.py loaddata 1-state-nogeo
    python manage.py loaddata 2-county-nogeo
    python manage.py loaddata 3-zipcode-nogeo

If you are running PostGIS and GeoDjango and wish to use geo-aware fixtures, see the download links under the **Fixture downloads** section, below.

## Resources

You can check Django's official documentation for more information about fixtures:

* The ["initial data" docs](http://docs.djangoproject.com/en/dev/howto/initial-data/) discuss loading the data and other ways you could do fixture loading (i.e. SQL dumps).
* [Serialization](http://docs.djangoproject.com/en/dev/topics/serialization/) deals with the "exporting" of data into a flat file. We're using the XML flavor and these are bzip'd to save on space, since Django can import bzip'd fixtures natively.

## Fixture downloads

We currently have the following fixture data:

* **1-state** - Corresponding to the State model
    * [Non-geo fixture](http://media1.mike.tig.as/files/20090907_nationbrowse_fixtures/1-state-nogeo.xml.bz2) (1.6 KB), lacking polygonal shape data.
    * [Full-size, geo-aware fixture](http://media1.mike.tig.as/files/20090907_nationbrowse_fixtures/1-state.xml.bz2) (7.6 MB).
* **2-county** - Corresponding to the County model
    * [Non-geo fixture](http://media1.mike.tig.as/files/20090907_nationbrowse_fixtures/2-county-nogeo.xml.bz2) (48 KB), lacking polygonal shape data.
    * [Full-size, geo-aware fixture](http://media1.mike.tig.as/files/20090907_nationbrowse_fixtures/2-county.xml.bz2) (66 MB).
* **3-zipcode** - Corresponding to the ZipCode model
    * [Non-geo fixture](http://media1.mike.tig.as/files/20090907_nationbrowse_fixtures/3-zipcode-nogeo.xml.bz2) (200 KB), lacking polygonal shape data.
    * The geo-aware data is split up into five fixtures, due to size:
        * [Full fixture A](http://media1.mike.tig.as/files/20090907_nationbrowse_fixtures/3-zipcode-A.xml.bz2) (92 MB)
        * [Full fixture B](http://media1.mike.tig.as/files/20090907_nationbrowse_fixtures/3-zipcode-B.xml.bz2) (149 MB)
        * [Full fixture C](http://media1.mike.tig.as/files/20090907_nationbrowse_fixtures/3-zipcode-C.xml.bz2) (100 MB)
        * [Full fixture D](http://media1.mike.tig.as/files/20090907_nationbrowse_fixtures/3-zipcode-D.xml.bz2) (134 MB)
        * [Full fixture E](http://media1.mike.tig.as/files/20090907_nationbrowse_fixtures/3-zipcode-E.xml.bz2) (52 MB)
