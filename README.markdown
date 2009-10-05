# CS4970 Capstone: NationBrowse

Repository for our Fall 2009 capstone project.

## (Python) Install Dependencies

These only represent "backend" requirements that must be installed on the server. Client-side libraries
(jQuery, OpenLayers, etc) are not covered by this list.

### For "basic" Django site, without geo-awareness.

* [Python](http://www.python.org/) 2.5 or 2.6
 * [SciPy](http://www.scipy.org/) & [NumPy](http://numpy.scipy.org/)
 * [MatPlotLib](http://matplotlib.sourceforge.net/)
 * [Python Imaging Library (PIL)](http://www.pythonware.com/products/pil/), maybe. Only if we use Django's [ImageField](http://docs.djangoproject.com/en/dev/ref/models/fields/#imagefield), which is not likely.
* [PostgreSQL](http://www.postgresql.org/) (optional -- can use SQLite instead for local development)
 * See below regarding GIS database requirement 
 
### For "full" site, including GIS-aware queries and the map rendering server.

* All of the above, and:
 * [PostgreSQL](http://www.postgresql.org/) (unlike above, this is absolutely required)
 * [PostGIS](http://postgis.refractions.net/) extensions to PostgreSQL
 * [Mapnik](http://mapnik.org/)
 * [TileCache](http://tilecache.org/)

## Resources

### Python language reference:

* [Official docs](http://docs.python.org/)
* [Rosetta Code](http://rosettacode.org/wiki/Category:Python) comparisons to other languages.

### Django reference:

* [Django official site](http://www.djangoproject.com/)
* [Official docs](http://docs.djangoproject.com/)

### Sites built in Python/Django:

* [The Maneater](http://www.themaneater.com/)
* [The Spokesman-Review](http://www.spokesman.com/)
* The Washington Post has been known to use Django for special online projects.

### Other code libraries or APIs:

* [jQuery](http://docs.jquery.com/Main_Page)
* [OpenLayers](http://trac.openlayers.org/wiki) ([example sites](http://openlayers.org/dev/examples/))
* [Mapnik](http://trac.mapnik.org/) ([example sites](http://mapnik.org/demo/))
* [SciPy](http://www.scipy.org/) (and the integrated [NumPy](http://numpy.scipy.org/)) will do statistical calculations for us.
* [MatPlotLib](http://matplotlib.sourceforge.net/) is an *awesome* library that creates graphs and charts in Python. MatPlotLib and SciPy go hand-in-hand (and are often bundled with one another).
* If we can find a way to integrate [WolframAlpha](http://www.wolframalpha.com/) search (or even just link to results), that could be useful.

## Prior art / alternatives

### Back-end
* [InstantAtlas](http://www.instantatlas.com/) is a proprietary and commercial product from [ESRI](http://www.esri.com/) that also creates shaded maps based on statistical data. In addition, InstantAtlas outputs the original data in tabular format.
* ESRI also owns and sells the ArcGIS suite, including the [ArcGIS Server](http://www.esri.com/products/index.html#2) which provides nearly the same map-rendering functionality as Mapnik.
* [MapServer](http://mapserver.org/) is another free and open-source tile renderer, like Mapnik.

### Web app implementations
* [ThisWeKnow](http://www.thisweknow.org/) allows browsing of Data.gov information — a very similar idea to this one. [Third place](http://sunlightlabs.com/blog/2009/apps-america-winners/) in the [Apps For America 2](http://sunlightlabs.com/contests/appsforamerica2/) contest (see below).
* [DataMasher](http://www.datamasher.org/) does direct comparisons between different datasets, but not necessarily in a statistically significant manner. [Won](http://sunlightlabs.com/blog/2009/apps-america-winners/) the [Apps For America 2](http://sunlightlabs.com/contests/appsforamerica2/) contest (see below).
* [EveryBlock](http://everyblock.com/) is a fairly renowned web app that uses the same pieces as above (OpenLayers, Mapnik, Django, etc). [This article](http://www.alistapart.com/articles/takecontrolofyourmaps) discusses the rationale behind EveryBlock using the "stack" of PostGIS, Mapnik, TileCache, and OpenLayers.
* [This Los Angeles Times mapping project](http://projects.latimes.com/mapping-la/neighborhoods/) is a [Census data](http://factfinder.census.gov/home/saff/main.html)-powered Web app that does a little bit of what we want — we'll want to use more varied data than them, and on a national scale.
* [Apps For America](http://www.sunlightlabs.com/contests/appsforamerica/) and [Apps For America 2](http://sunlightlabs.com/contests/appsforamerica2/) is a contest for sites built on [Data.gov](http://www.data.gov/)-supplied datasets. These are <b>all</b> open-source, though I don't think any of them use the same stack we do. Submitted apps for both contests are [here](http://www.sunlightlabs.com/contests/appsforamerica/apps/) and [here](http://sunlightlabs.com/contests/appsforamerica2/apps/).
* Some folks at Rensselaer Polytechnic Institute have a bunch of their own resources at [their data.gov-centered wiki](http://data-gov.tw.rpi.edu/wiki/Main_Page).
* [FiveThirtyEight](http://www.fivethirtyeight.com/) is an election coverage Web site that frequently uses maps and charts of election and poll data.
* The fine folks at the New York Times do maps quite a bit, including [this fine example of mapped civic data](http://projects.nytimes.com/crime/homicides/map) (map of all homicides in New York City).
