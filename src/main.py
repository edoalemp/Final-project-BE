"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import datetime
import os, random, math
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Person, Organization, Measure, Assignedmeasure, Data, Station
from sqlalchemy import func

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
    agrega una organizacion (POST), trae lista de organizaciones (GET)
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

        station1 = Station(name=body['name'], lattitude=body['lattitude'], longitude=body['longitude'], person_id=body['person_id'], description=body['description'], organization_id=body['organization_id'], streetaddress=body['streetaddress'], numberaddress=body['numberaddress'])
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
    edita una estación (PUT), borra una estacion (DELETE) y trae una estación (GET)
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
        if "streetaddress" in body:
            station1.streetaddress = body["streetaddress"]
        if "numberaddress" in body:
            station1.numberaddress = body["numberaddress"]

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
        if 'symbol' not in body:
            raise APIException('You need to specify the symbol', status_code=400)

        measure1 = Measure(name=body['name'], unit=body['unit'], symbol=body['symbol'])
        db.session.add(measure1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_measures = Measure.query.all()
        all_measures = list(map(lambda x: x.serialize(), all_measures))
        return jsonify(all_measures), 200

    return "Invalid Method", 404

@app.route('/measures/<int:measure_id>', methods=['PUT', 'DELETE', 'GET'])
def get_single_measure(measure_id):
    """
    edita una medida (PUT), borra una medida (DELETE) y trae una medida
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
        if "symbol" in body:
            measure1.symbol = body["symbol"]

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

    # GET request
    if request.method == 'GET':
        measure1 = Measure.query.get(measure_id)
        if measure1 is None:
            raise APIException('Measure not found', status_code=404)
        return measure1.serialize(), 200


    return "Invalid Method", 404


####   Mediciones Asignadas a estación   ####


@app.route('/assignedmeasures', methods=['POST', 'GET'])
def handle_assigned_measures():
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

    # GET request
    if request.method == 'GET':
        all_assignedmeasures = Assignedmeasure.query.all()
        all_assignedmeasures = list(map(lambda x: x.serialize(), all_assignedmeasures))
        return jsonify(all_assignedmeasures), 200

    return "Invalid Method", 404



@app.route('/assignedmeasures/<int:station_id>/<int:measure_id>/<string:date_from>/<string:date_to>', methods=['GET'])
def handle_data_measure(station_id, measure_id, date_from, date_to):
    """
    Trae los datos de una medición (GET)
    """

    # GET request
    if request.method == 'GET':

        s=date_from
        e=date_to
        datefrom = datetime.datetime(int(s[0:4]), int(s[4:6]), int(s[6:8]), int(s[8:10]), int(s[10:12]), int(s[12:14]))
        dateto= datetime.datetime(int(e[0:4]), int(e[4:6]), int(e[6:8]), int(e[8:10]), int(e[10:12]), int(e[12:14]))

        #Obtengo data con la id requerida
        datameasure = Assignedmeasure.query.filter(Assignedmeasure.station_id==station_id).filter(Assignedmeasure.measure_id==measure_id).first()

        #Obtengo la data necesaria filtrando por fechas y por la id que obtengo en el filtrado anterior
        values = Data.query.filter(Data.data_time_measure >= datefrom).filter(Data.data_time_measure <= dateto).filter(Data.assignedmeasure_id == datameasure.id )

        if values is None:
            raise APIException('Values not found', status_code=404)

        parsed_values = list(map(lambda x: x.serialize(), values))
        return jsonify(parsed_values), 200

    return "Invalid Method", 404


@app.route('/assignedmeasures/last', methods=['GET'])
def handle_last_data_measure():
    """
    Trae los datos de ultimas mediciones (GET)
    """

    # GET request
    if request.method == 'GET':

        all_assignedmeasures = Assignedmeasure.query.all()
        all_assignedmeasures = list(map(lambda x: x.serialize(), all_assignedmeasures))
        size=len(all_assignedmeasures)
        lastdata=[]
        items=[]
        for i in range(0,size):
            item={

                "data_time_measure":"",
                "data_value":"",
                "measure_id":"",
                "station_id":""
            }
            data=Data.query.filter(Data.assignedmeasure_id==all_assignedmeasures[i]["id"]).order_by(Data.data_time_measure.desc()).first()
            x=data.serialize()

            item["data_time_measure"]=x["data_time_measure"]
            item["data_value"]=x["data_value"]
            item["measure_id"]=all_assignedmeasures[i]["measure_id"]
            item["station_id"]=all_assignedmeasures[i]["station_id"]

            lastdata.append(item)

        if lastdata is None:
            raise APIException('Values not found', status_code=404)

        #lastdata = list(map(lambda x: x.serialize(), lastdata))
        return jsonify(lastdata), 200

    return "Invalid Method", 404

@app.route('/assignedmeasures/<int:assignedmeasure_id>', methods=['DELETE'])
def get_assigned_measures(assignedmeasure_id):
    """
    Borra una medición asignada a estación (DELETE)
    """

    # DELETE request
    if request.method == 'DELETE':

        values = Data.query.filter(Data.assignedmeasure_id == assignedmeasure_id).first()

        if values is None:
            raise APIException('Measure not found', status_code=404)

        db.session.delete(values)
        db.session.commit()

        assignedmeasure1 = Assignedmeasure.query.get(assignedmeasure_id)
        if values is None:
            raise APIException('Measure not found', status_code=404)
        db.session.delete(assignedmeasure1)
        db.session.commit()


        return "ok", 200

    return "Invalid Method", 404

@app.route('/stations/<int:station_id>/measures', methods=['GET'])
def get_assigned_measure_from_station(station_id):
    """
    Trae medidas asignadas desde estación (GET)
    """

    # GET request
    if request.method == 'GET':
        measures = Assignedmeasure.query.filter_by(station_id=station_id)
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
        stations = Assignedmeasure.query.filter_by(measure_id=measure_id)
        if stations is None:
            raise APIException('Stations not found', status_code=404)
        stations = list(map(lambda x: x.serialize(), stations))
        return jsonify(stations), 200



@app.route('/stations/fill', methods=['POST'])
def fill_stations():
    """
    Llena con estaciones (POST)
    """

    # POST request
    if request.method == 'POST':
        for i in range(3):
            station1 = Station(name="Estación"+str(i+1), lattitude=str(i+1), longitude=str(i+2), person_id=1, description="", organization_id=1, streetaddress=str(i+1), numberaddress=str(i+1))
            db.session.add(station1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

@app.route('/measures/fill', methods=['POST'])
def fill_measures():
    """
    Llena con medidas (POST)
    """

    # POST request
    if request.method == 'POST':
        for i in range(3):
            measures1 = Measure(name="medida"+str(i+1), unit="unidad"+str(i+1), symbol="símbolo"+str(i+1))
            db.session.add(measures1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

@app.route('/assignedmeasures/fill', methods=['POST'])
def fill_assignedmeasures():
    """
    Llena con mediciones (POST)
    """

    # POST request
    if request.method == 'POST':
        for i in range(3):
            for j in range(3):
                assignedmeasure1 = Assignedmeasure(measure_id=i+1, station_id=j+1)
                db.session.add(assignedmeasure1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

@app.route('/data/fill', methods=['POST'])
def fill_data():
    """
    Llena con mediciones (POST)
    """

    # POST request
    if request.method == 'POST':

        month=0
        for month in range (1,13):
            if month == 1 or month ==3 or month==5 or month==7 or month==8 or month==10 or month==12:
                lastday=32
            elif month ==4 or month==6 or month==9 or month==11:
                lastday=31
            else:
                lastday=29
            for day in range (1,lastday):
                for hour in range(0,24):
                    if month<10:
                        strmonth="0"+str(month)
                    else:
                        strmonth=str(month)

                    if day<10:
                        strday="0"+str(day)
                    else:
                        strday=str(day)

                    if hour<10:
                        strhour="0"+str(hour)
                    else:
                        strhour=str(hour)

                    date="2018"+"-"+strmonth+"-"+strday+" "+strhour+":00:00"
                    value=random.randint(-5,45)
                    data1=Data(data_value=value, data_time_measure=date, assignedmeasure_id=1)
                    db.session.add(data1)
        db.session.commit()

        x=0
        for month in range (1,13):
            if month == 1 or month ==3 or month==5 or month==7 or month==8 or month==10 or month==12:
                lastday=32
            elif month ==4 or month==6 or month==9 or month==11:
                lastday=31
            else:
                lastday=29
            for day in range (1,lastday):
                for hour in range(0,24):
                    if month<10:
                        strmonth="0"+str(month)
                    else:
                        strmonth=str(month)

                    if day<10:
                        strday="0"+str(day)
                    else:
                        strday=str(day)

                    if hour<10:
                        strhour="0"+str(hour)
                    else:
                        strhour=str(hour)

                    date="2018"+"-"+strmonth+"-"+strday+" "+strhour+":00:00"
                    value=100*math.sin(x)
                    x=x+1
                    data1=Data(data_value=value, data_time_measure=date, assignedmeasure_id=2)
                    db.session.add(data1)
        db.session.commit()

        x=0
        for month in range (1,13):
            if month == 1 or month ==3 or month==5 or month==7 or month==8 or month==10 or month==12:
                lastday=32
            elif month ==4 or month==6 or month==9 or month==11:
                lastday=31
            else:
                lastday=29
            for day in range (1,lastday):
                for hour in range(0,24):
                    if month<10:
                        strmonth="0"+str(month)
                    else:
                        strmonth=str(month)

                    if day<10:
                        strday="0"+str(day)
                    else:
                        strday=str(day)

                    if hour<10:
                        strhour="0"+str(hour)
                    else:
                        strhour=str(hour)

                    date="2018"+"-"+strmonth+"-"+strday+" "+strhour+":00:00"
                    value=100*math.sin(x)-(random.randint(-5,45))/2
                    x=x+1
                    data1=Data(data_value=value, data_time_measure=date, assignedmeasure_id=3)
                    db.session.add(data1)
        db.session.commit()

        month=0
        x=0
        for month in range (1,13):
            if month == 1 or month ==3 or month==5 or month==7 or month==8 or month==10 or month==12:
                lastday=32
            elif month ==4 or month==6 or month==9 or month==11:
                lastday=31
            else:
                lastday=29
            for day in range (1,lastday):
                for hour in range(0,24):
                    if month<10:
                        strmonth="0"+str(month)
                    else:
                        strmonth=str(month)

                    if day<10:
                        strday="0"+str(day)
                    else:
                        strday=str(day)

                    if hour<10:
                        strhour="0"+str(hour)
                    else:
                        strhour=str(hour)

                    date="2018"+"-"+strmonth+"-"+strday+" "+strhour+":00:00"
                    value=random.randint(-10,100)
                    data1=Data(data_value=value, data_time_measure=date, assignedmeasure_id=4)
                    db.session.add(data1)
        db.session.commit()

        x=0
        for month in range (1,13):
            if month == 1 or month ==3 or month==5 or month==7 or month==8 or month==10 or month==12:
                lastday=32
            elif month ==4 or month==6 or month==9 or month==11:
                lastday=31
            else:
                lastday=29
            for day in range (1,lastday):
                for hour in range(0,24):
                    if month<10:
                        strmonth="0"+str(month)
                    else:
                        strmonth=str(month)

                    if day<10:
                        strday="0"+str(day)
                    else:
                        strday=str(day)

                    if hour<10:
                        strhour="0"+str(hour)
                    else:
                        strhour=str(hour)

                    date="2018"+"-"+strmonth+"-"+strday+" "+strhour+":00:00"
                    value=75*math.cos(x)
                    x=x+1
                    data1=Data(data_value=value, data_time_measure=date, assignedmeasure_id=5)
                    db.session.add(data1)
        db.session.commit()

        x=0
        for month in range (1,13):
            if month == 1 or month ==3 or month==5 or month==7 or month==8 or month==10 or month==12:
                lastday=32
            elif month ==4 or month==6 or month==9 or month==11:
                lastday=31
            else:
                lastday=29
            for day in range (1,lastday):
                for hour in range(0,24):
                    if month<10:
                        strmonth="0"+str(month)
                    else:
                        strmonth=str(month)

                    if day<10:
                        strday="0"+str(day)
                    else:
                        strday=str(day)

                    if hour<10:
                        strhour="0"+str(hour)
                    else:
                        strhour=str(hour)

                    date="2018"+"-"+strmonth+"-"+strday+" "+strhour+":00:00"
                    value=25*math.sin(x)+25*(random.randint(-5,45))
                    x=x+1
                    data1=Data(data_value=value, data_time_measure=date, assignedmeasure_id=6)
                    db.session.add(data1)
        db.session.commit()


        for month in range (1,13):
            if month == 1 or month ==3 or month==5 or month==7 or month==8 or month==10 or month==12:
                lastday=32
            elif month ==4 or month==6 or month==9 or month==11:
                lastday=31
            else:
                lastday=29
            for day in range (1,lastday):
                for hour in range(0,24):
                    if month<10:
                        strmonth="0"+str(month)
                    else:
                        strmonth=str(month)

                    if day<10:
                        strday="0"+str(day)
                    else:
                        strday=str(day)

                    if hour<10:
                        strhour="0"+str(hour)
                    else:
                        strhour=str(hour)

                    date="2018"+"-"+strmonth+"-"+strday+" "+strhour+":00:00"
                    value=75+0.25*random.randint(-10,100)
                    data1=Data(data_value=value, data_time_measure=date, assignedmeasure_id=7)
                    db.session.add(data1)
        db.session.commit()

        x=0
        for month in range (1,13):
            if month == 1 or month ==3 or month==5 or month==7 or month==8 or month==10 or month==12:
                lastday=32
            elif month ==4 or month==6 or month==9 or month==11:
                lastday=31
            else:
                lastday=29
            for day in range (1,lastday):
                for hour in range(0,24):
                    if month<10:
                        strmonth="0"+str(month)
                    else:
                        strmonth=str(month)

                    if day<10:
                        strday="0"+str(day)
                    else:
                        strday=str(day)

                    if hour<10:
                        strhour="0"+str(hour)
                    else:
                        strhour=str(hour)

                    date="2018"+"-"+strmonth+"-"+strday+" "+strhour+":00:00"
                    value=75*math.cos(x)
                    x=x+1
                    data1=Data(data_value=value, data_time_measure=date, assignedmeasure_id=8)
                    db.session.add(data1)
        db.session.commit()

        x=0
        for month in range (1,13):
            if month == 1 or month ==3 or month==5 or month==7 or month==8 or month==10 or month==12:
                lastday=32
            elif month ==4 or month==6 or month==9 or month==11:
                lastday=31
            else:
                lastday=29
            for day in range (1,lastday):
                for hour in range(0,24):
                    if month<10:
                        strmonth="0"+str(month)
                    else:
                        strmonth=str(month)

                    if day<10:
                        strday="0"+str(day)
                    else:
                        strday=str(day)

                    if hour<10:
                        strhour="0"+str(hour)
                    else:
                        strhour=str(hour)

                    date="2018"+"-"+strmonth+"-"+strday+" "+strhour+":00:00"
                    value=25*math.sin(x)+25*math.cos(x)
                    x=x+1
                    data1=Data(data_value=value, data_time_measure=date, assignedmeasure_id=9)
                    db.session.add(data1)
        db.session.commit()


        return "ok", 200

    return "Invalid Method", 404







if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
