# CS4970 Capstone: NationBrowse

Repository for our Fall 2009 capstone project.

## Repository structure

For the purposes of the class project, our code lives in the following locations:

* Python-based, project-specific code
 * /django_server/server/nationbrowse/
* Templates for HTML, dynamic JS, other dynamically-generated text
 * /django_server/templates/
* Static HTML, Javascript, CSS
 * /django_server/static/
* In-progress, experimental code
 * /sandbox/

## (Python) Install Dependencies

These only represent "backend" requirements that must be installed on the server. Client-side libraries
(jQuery, OpenLayers, etc) are not covered by this list, since they're included or linked from the codebase.

### The basics: data browsing site, without geo-awareness.

* [Python](http://www.python.org/) 2.5 or 2.6
 * [SciPy](http://www.scipy.org/) & [NumPy](http://numpy.scipy.org/)
 * [MatPlotLib](http://matplotlib.sourceforge.net/)
 * [Python Imaging Library (PIL)](http://www.pythonware.com/products/pil/), maybe. Only if we use Django's [ImageField](http://docs.djangoproject.com/en/dev/ref/models/fields/#imagefield), which is not likely.
* Any [Django-supported databae backend](http://docs.djangoproject.com/en/dev/topics/install/#database-installation). We recommend [PostgreSQL](http://www.postgresql.org/).
 * But see below regarding GIS database requirements.
 
### For a full experience, including GIS-aware queries and map rendering.

* All of the above, and:
 * [PostgreSQL](http://www.postgresql.org/) (unlike above, this is absolutely required)
 * [PostGIS](http://postgis.refractions.net/) extensions to PostgreSQL
