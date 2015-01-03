# USA Cycling Database Tools

Tools for loading the USA Cycling Membership Database (otherwise known as "CSV files").

## Prerequisites

Install prerequisites libraries using `pip`:

    $ pip install -r requirements.txt

## Usage

### SQL

1. Create a database using any of [SQLAlchemy's supported database servers](http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#supported-databases)
2. Install any required Python database drivers for interfacing with your database server (i.e., `psycopg2` for PostgreSQL or `MySQL-Python` for MySQL, etc.)
3. Download the USAC CSV files from the [USAC website](http://www.usacycling.org/). You need the "New Universal Complete" CSV file for riders and the "All Clubs (1 row/team)" CSV file for clubs.
4. Run the `load_sql.py` script to load the CSV files into your database server:
        
        $ python load_sql.py <database_uri> \
        <path_to_usac_rider_csv> \
        <path_to_usac_clubs_csv>
   
   Substitute the appropriate database URI and file paths for your system.

### Redis

1. Start up a Redis server:

       $ redis-server

2. Download the USAC CSV files from the [USAC website](http://www.usacycling.org/). You need the "New Universal Complete" CSV file for riders and the "All Clubs (1 row/team)" CSV file for clubs.
3. Run the `load_redis.py` script to load the database files into memory:

        $ python load_redis.py <path_to_usac_rider_csv> <path_to_usac_clubs_csv>
        
### HTTP API

A demonstration REST API implemented in Flask is provided. It uses `libusac3`'s SQL backend primarily, but provides a few endpoints to the Redis backend for uses such as typeahead.

Basic endpoint overview:

* Redis:
	* `GET /api/rds/rider/<int:license_number>`: basic information about a rider (first name, last name, license number, associate clubs)
	* `GET /api/rds/rider/<int:license_number>/all`: get a complete rider object
	* `GET /api/rds/rider/search/<int:partial>`: search for license numbers similar to `partial`
* SQL:
	* `GET /api/sql/rider/<int:license_number>`: get a complete rider object
	* `GET /api/sql/rider/<int:license_number>/<relationship>`: get a complete club or team object related to a rider
		* `road_club`
		* `road_team`
		* `track_club`
		* `track_team`
		* `mtn_club`
		* `mtn_team`
		* `cx_club`
		* `cx_team`
		* `coll_club`: collegiate club