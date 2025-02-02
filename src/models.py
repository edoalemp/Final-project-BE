from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    persons = db.relationship('Person')

    def __repr__(self):
        return '<Organization %r>' % self.name

    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email

        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    stations = db.relationship('Station')

    def __repr__(self):
        return '<Person %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "organization": self.organization_id
        }

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    lattitude = db.Column(db.String(40), unique=True, nullable=False)
    longitude = db.Column(db.String(40), unique=True, nullable=False)
    streetaddress = db.Column(db.String(80), unique=True, nullable=False)
    numberaddress = db.Column(db.String(10), unique=True, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    assignedMeasures = db.relationship('Assignedmeasure')

    def __repr__(self):
        return '<Station %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lattitude": self.lattitude,
            "longitude": self.longitude,
            "streetaddress": self.streetaddress,
            "numberaddress": self.numberaddress,
            "responsible": self.person_id,
            "description": self.description,
            "organization": self.organization_id
        }

class Measure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    unit = db.Column(db.String(20), unique=True, nullable=False)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    assignedMeasures = db.relationship('Assignedmeasure')

    def __repr__(self):
        return '<Measure %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
            "symbol": self.symbol
        }

class Assignedmeasure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measure_id = db.Column(db.Integer, db.ForeignKey('measure.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    data = db.relationship('Data')

    def __repr__(self):
        return '<Assignedmeasure %r>' % self.measure_id

    def serialize(self):
        return {
            "id": self.id,
            "measure_id": self.measure_id,
            "station_id": self.station_id,

        }

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_value = db.Column(db.Float, unique=False, nullable=False)
    data_time_measure = db.Column(db.DateTime, unique=False, nullable=False)
    assignedmeasure_id = db.Column(db.Integer, db.ForeignKey('assignedmeasure.id'), nullable=True)

    def __repr__(self):
        return '<Data %r>' % self.data_value

    def serialize(self):
        return {
            "id":self.id,
            "data_value": self.data_value,
            "data_time_measure": self.data_time_measure
        }