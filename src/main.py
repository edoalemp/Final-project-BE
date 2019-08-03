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

@app.route('/organizations', methods=['POST', 'GET'])
def handle_organization():
    """
    agrega una organizacion (POST), trae lista de organizaciones
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'name' not in body:
            raise APIException('You need to specify the name', status_code=400)
        if 'address' not in body:
            raise APIException('You need to specify the address', status_code=400)
        if 'phone' not in body:
            raise APIException('You need to specify the phone', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)

        organization1 = Organization(name=body['name'], address=body['address'], phone=body['phone'], email=body['email'])
        db.session.add(organization1)
        db.session.commit()
        return "ok", 200

        # GET request
    if request.method == 'GET':
        all_organization = Organization.query.all()
        all_organization = list(map(lambda x: x.serialize(), all_organization))
        return jsonify(all_organization), 200

    return "Invalid Method", 404





@app.route('/persons', methods=['POST', 'GET'])
def handle_person():
    """
    agrega una persona (POST), trae una lista de personas (GET)
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'username' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'organization' not in body:
            raise APIException('You need to specify the organization', status_code=400)

        person1 = Person(username=body['username'], email=body['email'], organization=body['organization'])
        db.session.add(person1)
        db.session.commit()
        return "ok", 200

        # GET request
    if request.method == 'GET':
        all_people = Person.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200

    return "Invalid Method", 404







@app.route('/stations', methods=['POST', 'GET'])
def handle_station():
    """
    Trae lista de estaciones (GET) y agrega una estación (POST)
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
        if 'responsible' not in body:
            raise APIException('You need to specify the responsible', status_code=400)
        if 'organization' not in body:
            raise APIException('You need to specify the organization', status_code=400)


        station1 = Station(name=body['name'], lattitude=body['lattitude'], longitude=body['longitude'], responsible=body['responsible'], organization=body['organization'])
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
def get_single_station(station_id):
    """
    edita una estación (PUT) y borra una estacion (DELETE)
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        station1 = Station.query.get(station_id)
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
