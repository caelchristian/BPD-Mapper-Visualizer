from . import db
from flask_login import UserMixin
# from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    salt = db.Column(db.String(150))
    access = db.Column(db.String(5))
    attempts = db.Column(db.Integer)
    
    
class Arrest(db.Model):
    __tablename__ = "Arrests"
    
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
    mental_health = db.Column(db.Integer)
    drug_related = db.Column(db.Integer)
    dv_related = db.Column(db.Integer)
    alcohol_related = db.Column(db.Integer)
    areaname = db.Column(db.String(20))
    latitude = db.Column(db.String(12))
    longitude = db.Column(db.String(12))
    district = db.Column(db.String(30))
    priority = db.Column(db.String(15))
    
# class Stop(db.Model):
#     objectid = db.Column(db.Integer, primary_key=True)
#     incident_number = db.Column(db.String(20), unique=True)
#     call_type = db.Column(db.String(20))
#     call_time = db.Column(db.String(20))
#     race = db.Column(db.String(20))
#     gender = db.Column(db.String(20))
#     age = db.Column(db.Integer)

#     charge = db.Column(db.String(150))
#     most_serious = db.Column(db.Integer)
#     felony = db.Column(db.Integer)
#     violent = db.Column(db.Integer)
#     category = db.Column(db.Integer)