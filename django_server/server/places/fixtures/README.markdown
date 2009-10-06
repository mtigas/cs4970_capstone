# Fixtures!

The fun and easy way to share and load "fixed" data.

We currently have the following fixture data:

* **1-state**: Provides some basic data for the 50 states and 9 US-related territories:
  * Name
  * Poly — This is the [GeoDjango](http://geodjango.org/docs/) MultiPolygonField that represents the shape of the given state or territory. If you aren't using a GIS-aware database, it just gets stored as a big ol' text field. If you are, then [GeoDjango's API](http://geodjango.org/docs/geos.html) will work on this field.
  * [FIPS code](http://en.wikipedia.org/wiki/Federal_Information_Processing_Standard) — Census data uses this as the state's ID. Or rather, this is the value of the "foreign key" for state information.
  * USPS abbreviation
  * Associated Press abbreviation

To use this, make sure you have a database to work with. (The following commands assume you're working in the `server/capstone` directory.)

    python manage.py syncdb

And then run this to load the actual data:

    python manage.py loaddata 1-state

You can check Django's official documentation for more:

* The [initial data docs](http://docs.djangoproject.com/en/dev/howto/initial-data/) discuss loading the data and other ways you could do fixture loading.
* [Serialization](http://docs.djangoproject.com/en/dev/topics/serialization/) deals with the "exporting" of data into a flat file. We're using the XML flavor (though see section below for a caveat).
