from . import db
from flask_login import UserMixin
# from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    salt = db.Column(db.String(150))
    access = db.Column(db.String(5))
    attempts = db.Column(db.Integer)
    
    
class Arrest(db.Model):
    objectid = db.Column(db.Integer, primary_key=True)
    incident_number = db.Column(db.String(20), unique=True)
    arrest_date = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    race = db.Column(db.String(20))
    age = db.Column(db.Integer)
    charge = db.Column(db.String(150))
    most_serious = db.Column(db.Integer)
    felony = db.Column(db.Integer)
    violent = db.Column(db.Integer)
    category = db.Column(db.Integer)
    
    
class Incident(db.Model):
    objectid = db.Column(db.Integer, primary_key=True)
    incident_number = db.Column(db.String(20), unique=True)
    call_type = db.Column(db.String(50))
    call_type_group = db.Column(db.String(50))
    call_time = db.Column(db.String(20))
    street = db.Column(db.String(50))
    call_origin = db.Column(db.String(20))
    mental_health = db.Column(db.Integer)
    drug_related = db.Column(db.Integer)
    dv_related = db.Column(db.Integer)
    alcohol_related = db.Column(db.Integer)
    area = db.Column(db.String(20))
    areaname = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    hour_ = db.Column(db.String(5))
    dayofweek = db.Column(db.String(10))
    ward = db.Column(db.String(20))
    district = db.Column(db.String(30))
    priority = db.Column(db.String(15))
    month_ = db.Column(db.String(10))
    year_ = db.Column(db.Integer)