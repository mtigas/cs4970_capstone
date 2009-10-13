## Creating the database

Some notes on setting up the GIS-aware database on our demo server. This is only for initial setup.

We're assuming a user and database named `cs4970_capstone`. Assuming the user and DB have already
been created, and that the user is the "owner" of the database. This is how you'd do that:

    createuser -sDR cs4970_capstone
    createdb -E UTF-8 -O cs4970_capstone cs4970_capstone

Note that in our setup, the user is able to log in only locally, but "trusted" without a password
when logging in locally. This is set up semi-insecurely, since access to the server shell means
full access to this database, but that's fine since our configuration files are stored in a public repository.
Production-class databases should probably be more careful.

    createlang -U cs4970_capstone -d cs4970_capstone plpgsql
    psql -U cs4970_capstone -d cs4970_capstone -f /usr/share/postgresql-8.3-postgis/lwpostgis.sql
    psql -U cs4970_capstone -d cs4970_capstone -f /usr/share/postgresql-8.3-postgis/spatial_ref_sys.sql

Note that the location of `lwpostgis.sql` and `spatial_ref_sys.sql` may vary from system to system.
The above paths reflect the default Ubuntu installation of `postgresql-8.3` and `postgresql-8.3-postgis`.
