"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Person, Organization, Measure, Assignedmeasure, Data, Station

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/stations', methods=['POST', 'GET'])
def handle_person():
    """
    Trae lista de estaciones (GET) y agrega una estación (PUT)
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'name' not in body:
            raise APIException('You need to specify the name', status_code=400)
        if 'lattitude' not in body:
            raise APIException('You need to specify the lattitude', status_code=400)
        if 'longitude' not in body:
            raise APIException('You need to specify the longitude', status_code=400)
        if 'responsibleuser' not in body:
            raise APIException('You need to specify the responsibleuser', status_code=400)
        if 'orzanization' not in body:
            raise APIException('You need to specify the orzanization', status_code=400)
        if 'assignedMeasure' not in body:
            raise APIException('You need to specify the assignedMeasure', status_code=400)

        station1 = Station(name=body['name'], lattitude=body['lattitude'], longitude=body['longitude'], responsibleuser=body['responsibleuser'], organization=body['organization'], assignedMeasure=body['assignedmeasure'])
        db.session.add(station1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_stations = Station.query.all()
        all_stations = list(map(lambda x: x.serialize(), all_stations))
        return jsonify(all_stations), 200

    return "Invalid Method", 404


@app.route('/stations/<int:station_id>', methods=['PUT', 'DELETE'])
def get_single_person(station_id):
    """
    edita una estación (PUT) y borra una estacion (DELETE)
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        station1 = Person.query.get(station_id)
        if station1 is None:
            raise APIException('Station not found', status_code=404)

        if "name" in body:
            station1.name = body["name"]
        if "lattitude" in body:
            station1.lattitude = body["lattitude"]
        if "longitude" in body:
            station1.longitude = body["longitude"]
        if "responsibleuser" in body:
            station1.responsibleuser = body["responsibleuser"]
        if "description" in body:
            station1.description = body["description"]
        if "organization" in body:
            station1.organization = body["organization"]
        db.session.commit()

        return jsonify(station1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        station1 = Station.query.get(station_id)
        if station1 is None:
            raise APIException('Station not found', status_code=404)
        db.session.delete(station1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
