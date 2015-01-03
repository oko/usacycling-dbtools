from flask import Blueprint, json, Response


sql_api = Blueprint('sql', __name__)


@sql_api.record
def record(state):
    db = state.app.config.get("USACDB_SQLALCHEMY")

    if db is None:
        raise Exception("The USAC SQL API blueprint requires that you provide a Flask-SQLAlchemy database object via"
                        "the USACDB_SQLALCHEMY configuration key")

    from libusac3 import sql_base
    sql_base.Base = db.Model


def object_not_found(obj_class, pk):
    return Response(
        json.dumps({"error": True, "status": 404, "code": "ERR_OBJ_NOT_FOUND", "obj_class": obj_class, "pk": pk}),
        status=404)


@sql_api.route('/riders/<int:license_number>')
def get_rider(license_number):
    from libusac3.sql import Rider

    rider = Rider.query.get(license_number)
    if rider is not None:
        print(rider.__dict__)
        return json.jsonify()
    else:
        return object_not_found("Rider", license_number)
