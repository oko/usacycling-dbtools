import datetime
import sys

import libusac3.http.default_config

from flask import Flask, Response, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

from redis import Redis
from libusac3.util import RIDER_TRANSFORMS, CLUB_TEAM_TRANSFORMS

app = Flask(__name__)
app.config.from_object(libusac3.http.default_config)
try:
    app.config.from_envvar("USACDB_HTTP_CONFIG")
except RuntimeError:
    sys.stderr.write("INFO: did not find an environment variable $USAC_HTTP_CONFIG, using default settings\n")

if app.config["USACDB_ENABLE_SQL"]:
    db = SQLAlchemy(app)

    import libusac3.sql_base

    libusac3.sql_base.Base = db.Model

    from libusac3.sql import Club, Team, Rider

    manager = APIManager(app, flask_sqlalchemy_db=db)

    manager.create_api(Club, methods=['GET'], collection_name="club", url_prefix="/api/sql")
    manager.create_api(Team, methods=['GET'], collection_name="team", url_prefix="/api/sql")
    manager.create_api(Rider, methods=['GET'], collection_name="rider", url_prefix="/api/sql")

if app.config["USACDB_ENABLE_REDIS"]:
    rds = Redis(host=app.config["USACDB_REDIS_HOST"], port=app.config["USACDB_REDIS_PORT"])

    def object_not_found(obj_class, pk):
        return Response(
            json.dumps({"error": True, "status": 404, "code": "ERR_OBJ_NOT_FOUND", "obj_class": obj_class, "pk": pk}),
            status=404, content_type="application/json")

    def get_club(cid):
        rdata = rds.hgetall("club:%d" % int(cid))
        if not rdata:
            return None
        ad = {}
        for key, func in CLUB_TEAM_TRANSFORMS:
            if key is None:
                continue
            bkey = key.encode('utf-8')
            ad[key] = func(rdata[bkey].decode())
        return ad

    def get_team(tid):
        rdata = rds.hgetall("team:%d" % int(tid))
        if not rdata:
            return None
        ad = {}
        for key, func in CLUB_TEAM_TRANSFORMS:
            if key is None:
                continue
            bkey = key.encode('utf-8')
            ad[key] = func(rdata[bkey].decode())
        ad["club"] = get_club(ad["club_id"])
        return ad

    def get_rider(lic):
        rdata = rds.hgetall("rider:%d" % int(lic))
        if not rdata:
            return None
        ad = {}
        for key, func in RIDER_TRANSFORMS:
            if key is None:
                continue
            bkey = key.encode('utf-8')
            ad[key] = func(rdata[bkey].decode())
            if type(ad[key]) is datetime.date:
                ad[key] = ad[key].isoformat()
            if "club_id" in key and ad[key] is not None:
                ad[key[:-3]] = get_club(ad[key])
            if "team_id" in key and ad[key] is not None:
                ad[key[:-3]] = get_team(ad[key])
        return ad

    DISCIPLINES = ("road", "track", "mtn", "cx", "coll")

    @app.route('/api/rds/rider/<int:license_number>')
    def rds_get_rider(license_number):
        """
        Get basic information of a specific rider based on their license number

        :param license_number: the license number of the rider to retrieve
        :return: specific information about the rider
        """
        rider = get_rider(license_number)
        if rider:
            jsondict = {
                "first_name": rider["first_name"],
                "last_name": rider["last_name"],
                "license": rider["license"],
            }
            for discipline in DISCIPLINES:
                if rider["%s_club_id" % discipline]:
                    jsondict["%s_club" % discipline] = get_club(rider["%s_club_id" % discipline])["club_name"]
                else:
                    jsondict["%s_club" % discipline] = None
            return json.jsonify(jsondict)
        else:
            return object_not_found("Rider", license_number)

    @app.route('/api/rds/rider/<int:license_number>/all')
    def rds_get_rider_all(license_number):
        """
        Get all information of a specific rider based on their license number

        :param license_number: the license number of the rider to retrieve
        :return: all information about the rider
        """
        rider = get_rider(license_number)
        if rider:
            return json.jsonify(rider)
        else:
            return object_not_found("Rider", license_number)

    @app.route('/api/rds/rider/search/<string:partial>')
    def rds_search_rider(partial):
        """
        Search for riders with license numbers like `partial`

        :param partial: a partial license number
        :return: a list of potential matches
        """
        keys = rds.keys("rider:%s?" % partial)
        return json.jsonify({"matches": list(map(lambda k: k.decode('utf-8'), keys))})

if __name__ == "__main__":
    app.run(debug=True)