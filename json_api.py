from flask import Flask, request, abort, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/usacdb'
"""
import libusac2.sql_base
db = SQLAlchemy(app)
libusac2.sql_base.ModelBase = db.Model

from libusac2.sql import Rider, Club, Team

@app.route('/rider/<int:license>/')
def get_rider(license):
    r = Rider.query.get(license)
    if r is None:
        abort(404)
    else:
        return jsonify({
            'license_number': r.license_number,
            'first_name': r.first_name,
            'last_name': r.last_name,
            'racing_age': r.racing_age,
            'location': "%s, %s" % (r.city, r.state),
        }),
        """
from redis import Redis
rds = Redis()

@app.route('/rider/<int:lic>/')
def get_rider(lic):
    r = rds.hgetall('rider:%d'%lic)
    return jsonify(r)

@app.route('/rider/search/<int:lic>/')
def search_riders(lic):
    if lic < 1000:
        return jsonify({'error': 'search string too short'}), 404
    if lic > 1000000:
        return jsonify({'error': 'search string too long'}), 404

    ks = rds.keys('rider:%d*'%lic)
    rs = []
    for k in ks:
        rs.append(rds.hgetall(k))
        if len(rs) > 10:
            break
    return jsonify({'riders':rs})

if __name__ == "__main__":
    app.run(debug=True)