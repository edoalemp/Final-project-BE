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


####   Organizaciones   ####


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


@app.route('/organizations/<int:organization_id>/people', methods=['GET'])
def handle_organization_people(organization_id):
    """
    Trae una lista de personas de una organización
    """

        # GET request
    if request.method == 'GET':
        organization_people = Person.query.filter(organization_id=organization_id)
        organization_people = list(map(lambda x: x.serialize(), organization_people))
        return jsonify(organization_people), 200

    return "Invalid Method", 404


####   Personas   ####


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
        if 'organization_id' not in body:
            raise APIException('You need to specify the organization', status_code=400)

        person1 = Person(username=body['username'], email=body['email'], organization_id=body['organization_id'])
        db.session.add(person1)
        db.session.commit()
        return "ok", 200

        # GET request
    if request.method == 'GET':
        all_people = Person.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200

    return "Invalid Method", 404


####   Estaciones    ####


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
        if 'person_id' not in body:
            raise APIException('You need to specify the person_id', status_code=400)
        if 'organization_id' not in body:
            raise APIException('You need to specify the organization_id', status_code=400)
        if 'streetaddress' not in body:
            raise APIException('You need to specify the street address', status_code=400)
        if 'numberaddress' not in body:
            raise APIException('You need to specify the number address', status_code=400)

        station1 = Station(name=body['name'], lattitude=body['lattitude'], longitude=body['longitude'], person_id=body['person_id'], organization_id=body['organization_id'], streetaddress=body['streetaddress'], numberaddress=body['numberaddress'])
        db.session.add(station1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_stations = Station.query.all()
        all_stations = list(map(lambda x: x.serialize(), all_stations))
        return jsonify(all_stations), 200

    return "Invalid Method", 404

@app.route('/stations/<int:station_id>', methods=['PUT', 'DELETE', 'GET'])
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
        if "person_id" in body:
            station1.person_id = body["person_id"]
        if "description" in body:
            station1.description = body["description"]
        if "organization_id" in body:
            station1.organization_id = body["organization_id"]
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

    # GET request
    if request.method == 'GET':
        station1 = Station.query.get(station_id)
        if station1 is None:
            raise APIException('Station not found', status_code=404)
        return station1.serialize(), 200

    return "Invalid Method", 404


####   Medidas    ####


@app.route('/measures', methods=['POST', 'GET'])
def handle_measure():
    """
    Trae lista de medida (GET) y agrega una medida (POST)
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'name' not in body:
            raise APIException('You need to specify the name', status_code=400)
        if 'unit' not in body:
            raise APIException('You need to specify the unit', status_code=400)

        measure1 = Measure(name=body['name'], unit=body['unit'])
        db.session.add(measure1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_measures = Measure.query.all()
        all_measures = list(map(lambda x: x.serialize(), all_measures))
        return jsonify(all_measures), 200

    return "Invalid Method", 404

@app.route('/measures/<int:measure_id>', methods=['PUT', 'DELETE'])
def get_single_measure(measure_id):
    """
    edita una medida (PUT) y borra una medida (DELETE)
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        measure1 = Measure.query.get(measure_id)
        if measure1 is None:
            raise APIException('Measure not found', status_code=404)

        if "name" in body:
            measure1.name = body["name"]
        if "unit" in body:
            measure1.unit = body["unit"]

        db.session.commit()

        return jsonify(measure1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        measure1 = Measure.query.get(measure_id)
        if measure1 is None:
            raise APIException('Measure not found', status_code=404)
        db.session.delete(measure1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


####   Mediciones Asignadas a estación   ####


@app.route('/assignedmeasures', methods=['POST'])
def handle_assigned_measure():
    """
    asigna una medicion a estación (POST)
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'station_id' not in body:
            raise APIException('You need to specify the station_id', status_code=400)
        if 'measure_id' not in body:
            raise APIException('You need to specify the measure_id', status_code=400)

        assignedmeasure1 = Assignedmeasure(station_id=body['station_id'], measure_id=body['measure_id'])
        db.session.add(assignedmeasure1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

@app.route('/assignedmeasures/<int:assignedmeasure_id>', methods=['DELETE'])
def get_assigned_measures(assignedmeasure_id):
    """
    Borra una medición asignada a estación (DELETE)
    """

    # DELETE request
    if request.method == 'DELETE':
        assignedmeasure1 = Assignedmeasure.query.get(assignedmeasure_id)
        if assignedmeasure1 is None:
            raise APIException('Measure not found', status_code=404)
        db.session.delete(assignedmeasure1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

@app.route('/stations/<int:station_id>/assignedmeasures', methods=['GET'])
def get_assigned_measure_from_station(station_id):
    """
    Trae medidas asignadas desde estación (GET)
    """

    # GET request
    if request.method == 'GET':
        measures = Assignedmeasure.query.filter(station_id=station_id)
        if measures is None:
            raise APIException('Measures not found', status_code=404)
        measures = list(map(lambda x: x.serialize(), measures))
        return jsonify(measures), 200

@app.route('/measures/<int:measure_id>/stations', methods=['GET'])
def get_stations_with_measures(measure_id):
    """
    Trae estaciones con la medición asignada (GET)
    """

    # GET request
    if request.method == 'GET':
        stations = Assignedmeasure.query.filter(measure_id=measure_id)
        if stations is None:
            raise APIException('Stations not found', status_code=404)
        stations = list(map(lambda x: x.serialize(), stations))
        return jsonify(stations), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
