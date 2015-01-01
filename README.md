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
4. Run `python load_sql.py <database_uri> <path_to_usac_rider_csv> <path_to_usac_clubs_csv>` (substituting the appropriate values for each `<...>` section) to load the CSVs into the database.
