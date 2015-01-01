from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from attrdict import AttrDict
import sys

import argparse

parser = argparse.ArgumentParser(description='Generate an analysis of the current USAC member database')
parser.add_argument('uri', type=str, help='an SQL database URI')
parser.add_argument('--format', type=str, help="'markdown' or 'json' output format", default='markdown')
args = parser.parse_args()

engine = create_engine(args.uri)
Session = sessionmaker(bind=engine)
session = Session()

from libusac3.sql import Base, Rider, Club, Team

Base.metadata.create_all(bind=engine)

rq = session.query(Rider)
riders = rq.all()

from collections import OrderedDict

def by_param(result, c1, c2):
    d = OrderedDict()
    for r in result:
        d[r[c1]] = int(r[c2])
    return d


def riders_by_discipline(disc):
    return by_param(engine.execute("""
    SELECT %(disc)s_cat , COUNT(*) as num_riders
      FROM usac_rider AS r
      WHERE r.%(disc)s_cat IN (0,1,2,3,4,5)
      GROUP BY r.%(disc)s_cat
      ORDER BY r.%(disc)s_cat;
    """ % {'disc': disc}),
        "%s_cat" % disc, "num_riders"
    )

def print_riders_by_disc(disc):
    by_param_out = riders_by_discipline(disc)
    print("### Riders by %s category\n" % disc)
    for cat, count in by_param_out.items():
        print(" * **%s**: %d riders" % ("Pro" if not cat else "Cat %d" % int(cat), count))
    print()

riders_count = rq.count()
riders_count_male = rq.filter_by(gender="M").count()
riders_count_female = rq.filter_by(gender="F").count()
riders_count_by_racing_age = by_param(
    engine.execute("""
SELECT t.age AS over_age, SUM(t.num) as num_riders
    FROM (
        SELECT
            /* ROUND does traditional rounding based on halves
               so subtract 5 to keep the buckets on 10-year bounds */
            ROUND(racing_age - 5, -1) as age,
            COUNT(*) as num
        FROM usac_rider
            GROUP BY racing_age
            ORDER BY racing_age
    ) AS t
GROUP BY t.age
ORDER BY t.age;"""),
    "over_age", "num_riders"
)
riders_count_by_state = by_param(
    engine.execute("""SELECT state, COUNT(*) FROM usac_rider GROUP BY state ORDER BY state;"""),
    "state", "count"
)
if args.format == 'markdown':
    print("### Total riders: %d" % riders_count)
    print(" * **Male**: %d" % riders_count_male)
    print(" * **Female**: %d" % riders_count_female)
    print()
    print("### Riders by racing age:")
    for age, count in riders_count_by_racing_age.items():
        print(" * **%d-%d**: %d riders" % (age, age+10, count))
    print()
    print_riders_by_disc("road")
    print_riders_by_disc("track")
    print_riders_by_disc("cx")
    print("### Riders by state:")
    for state, count in riders_count_by_state.items():
        print(" * **%s**: %d riders" % (state, count))
else:
    # TODO: implement JSON output support
    sys.stderr.writeline("ERROR: JSON output not yet supported")
