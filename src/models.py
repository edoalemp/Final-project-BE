from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    persons = db.relationship('Address')

    def __repr__(self):
        return '<Organization %r>' % self.name

    def serialize(self):
        return {
            "name": self.name,
            "email": self.email
        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    organization = db.Column(db.Integer, db.ForeignKey('organization.id'),
        nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email
        }

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    lattitude = db.Column(db.String(80), unique=True, nullable=False)
    longitude = db.Column(db.String(80), unique=True, nullable=False)
    responsibleUser = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=True)
    organization = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    assignedMeasure = db.relationship('AssignedMeasure')

    def __repr__(self):
        return '<Station %r>' % self.name

    def serialize(self):
        return {
            "name": self.name
        }

class Measure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    unit = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return '<Measure %r>' % self.name

    def serialize(self):
        return {
            "name": self.name
        }

class AssignedMeasure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stations = db.Column(db.Integer, db.ForeignKey('station.id'),
        nullable=False)
    def __repr__(self):
        return '<Measure %r>' % self.name

    def serialize(self):
        return {
            "name": self.name
        }