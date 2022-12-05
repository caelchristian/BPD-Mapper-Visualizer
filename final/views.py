from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import sqlite3
from . import db, get_db_connection
from sqlalchemy import insert, create_engine
from sqlalchemy.orm import Session
import json
from .auth import get_strong_password
from .models import User, Arrests, Incidents

views = Blueprint('home', __name__)
engine = create_engine("sqlite:///data.db")


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/suggest_password/', methods=['GET', 'POST'])
def get_password():
    print("Suggested Password: " + str(get_strong_password))
    return render_template("auth.html", user=current_user)


@views.route('/incident_form', methods=['GET', 'POST'])
def incident_form():
    table_name = "incidents"
    if request.method == 'POST':   
        any_none_values = False
        for key, val in request.form.items():
            # unchecked buttons are not keys in dict
            # exclude submit button
            if val == "" and key != "button":
                any_none_values = True
                    
        if not any_none_values:
            conn = get_db_connection()
            res = conn.execute(f"""
                        SELECT MAX(objectid)
                        FROM {table_name}
                        """)
            # max objectid+1 is new object id
            objectid = str(int(res.fetchone()[0] + 1))
            
            res = conn.execute(f"""
                            SELECT MAX(incident_number)
                            FROM {table_name}
                            """)
            # next incident number is max + 1
            incident_number = str(int(res.fetchone()[0]) + 1)
        
            call_type = request.form.get("call_type")
            call_type_group = request.form.get("call_type_group")
            call_time = request.form.get("call_time")
            street = request.form.get("street")
            
            if request.form.get("mental_health_related") != None:
                mental_health = 1
            else:
                mental_health = 0
                
            if request.form.get("drug_related") != None:
                drug_related = 1
            else:
                drug_related = 0
                
            if request.form.get("dv_related") != None:
                dv_related = 1
            else:
                dv_related = 0
                
            if request.form.get("alcohol_related") != None:
                alcohol_related = 1
            else:
                alcohol_related = 0
                
            areaname = request.form.get("area_name")
            latitude = request.form.get("latitude")
            longitude = request.form.get("longitude")
            district = request.form.get("district")
            priority = request.form.get("priority")
            
            # print(res.fetchall())
            c = conn.cursor()
            conn.execute(f"INSERT INTO incidents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (objectid, incident_number, call_type,
                call_type_group, call_time, street,
                mental_health, drug_related, dv_related,
                alcohol_related, areaname, latitude,
                longitude, district, priority))
            conn.commit()
            flash("Successfully inserted into table!", category="info")
        else:
            flash("One or more text box values are empty", category="error")

    return render_template("incident_form.html", user=current_user)


@views.route('/arrest_form', methods=['GET', 'POST'])
def form():
    table_name = "arrests"
    if request.method == 'POST':   
        any_none_values = False
        for key, val in request.form.items():
            # unchecked buttons are not keys in dict
            # exclude submit button
            print(key,":",val)
            if val == "" and key != "button":
                any_none_values = True
                    
        if not any_none_values:
            conn = get_db_connection()
            res = conn.execute(f"""
                        SELECT MAX(objectid)
                        FROM {table_name}
                        """)
            # max objectid+1 is new object id
            objectid = str(int(res.fetchone()[0] + 1))
            
            res = conn.execute(f"""
                            SELECT MAX(incident_number)
                            FROM {table_name}
                            """)
            # next incident number is max + 1
            incident_number = str(int(res.fetchone()[0]) + 1)
        
            arrest_date = request.form.get("date")
            gender = request.form.get("gender")
            race = request.form.get("race")
            age = request.form.get("age")
            charge = request.form.get("charge")
            
            if request.form.get("most_serious") != None:
                most_serious = 1
            else:
                most_serious = 0
                
            if request.form.get("felony") != None:
                felony = 1
            else:
                felony = 0
                
            if request.form.get("violent") != None:
                violent = 1
            else:
                violent = 0
                
            category = request.form.get("category")
            
            # print(res.fetchall())
            c = conn.cursor()
            conn.execute(f"INSERT INTO arrests VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (objectid, incident_number, arrest_date,
                gender, race, age, charge, most_serious,
                felony, violent, category))
            conn.commit()
            flash("Successfully inserted into table!", category="info")
        else:
            flash("One or more text box values are empty", category="error")
    return render_template("arrest_form.html", user=current_user)


# incident = Incident(
#     objectid = objectid,
#     incident_number = incident_number,
#     arrest_date = dict.get("arrest_date"),
#     gender = dict.get("gender"),
#     race = dict.get("race"),
#     age = dict.get("age"),
#     charge = dict.get("charge"),
#     most_serious = dict.get("most_serious"),
#     felony = dict.get("felony"),
#     violent = dict.get(["violent"]),
#     category = dict.get(["category"])
#     )


# incident_dict["call type"] = request.form.get("call_type")
# incident_dict["call type group"] = request.form.get("call_type_group")
# incident_dict["call time"] = request.form.get("call_time")
# incident_dict["call type"] = request.form.get("call_type")
# incident_dict["mental health related"] = request.form.get("mental_health_related")
# incident_dict["drug related"] = request.form.get("drug_related")
# incident_dict["domestic violence related"] = request.form.get("dv_related")
# incident_dict["alcohol related"] = request.form.get("alcohol_related")
# incident_dict["area"] = request.form.get("area")
# incident_dict["area name"] = request.form.get("area_name")
# incident_dict["area name"] = request.form.get("area_name")