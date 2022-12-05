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
def form():
    dict = {}
    table_name = "incidents"
    if request.method == 'POST':   
        with Session(engine) as session:
            
            any_none_values = False
            
            for key, val in request.form.items():
                temp = str(val)
                parsed = temp[1 : len(temp) - 2]
                print(temp)
                dict[key] = "" + parsed
                
                # unchecked buttons are not keys in dict
                # exclude submit button
                if val == "" and key != "button":
                    any_none_values = True
                        
            if not any_none_values:
                        
                conn = get_db_connection()
                    
                # max objectid+1 is new object id
                res = conn.execute("""SELECT * FROM incidents""")
                # print(res.fetchall()) 
                
                res = conn.execute(f"""
                            SELECT MAX(objectid)
                            FROM {table_name}
                            """)
                
                temp = str(res.fetchone()[0])
                
                # weird parsing thing
                objectid = int(temp[1:len(temp)-2])
                
                res = conn.execute(f"""
                                SELECT MAX(incident_number)
                                FROM {table_name}
                                """)

                temp = str(res.fetchone()[0])
                # weird parsing thing
                incident_number = int(temp[1:len(temp)-2]) + 1
                
                # next incident number is max + 1
                # print(res.fetchone())
                # print(session)
            
                objectid = objectid,
                incident_number = incident_number,
                call_type = dict.get("call_type"),
                call_type_group = dict.get("call_type_group"),
                call_time = dict.get("call_time"),
                street = dict.get("street"),
                
                if dict.get("street") != None:
                    mental_health = 1
                else:
                    mental_health = 0
                    
                if dict.get("drug_related") != None:
                    drug_related = 1
                else:
                    drug_related = 0
                    
                if dict.get("dv_related") != None:
                    dv_related = 1
                else:
                    dv_related = 0
                    
                if dict.get("alcohol_related") != None:
                    alcohol_related = 1
                else:
                    alcohol_related = 0
                    
                areaname = dict.get("areaname"),
                latitude = dict.get("latitude"),
                longitude = dict.get("longitude"),
                district = dict.get("district"),
                priority = dict.get("district"),
                
                print(objectid, str(incident_number), str(call_type),
                    str(call_type_group), str(call_time), str(street),
                    str(mental_health), str(drug_related), str(dv_related),
                    str(alcohol_related), str(areaname), str(latitude),
                    str(longitude), str(district), str(priority))
                
                # print(res.fetchall())
                c = conn.cursor()
                conn.execute(f"INSERT INTO incidents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (objectid, incident_number, call_type,
                    call_type_group, call_time, street,
                    mental_health, drug_related, dv_related,
                    alcohol_related, areaname, latitude,
                    longitude, district, priority))

                
                conn.commit()
                            
                print(dict)
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
            # else:
            #     flash("One or more entered values were empty")
                    
                
    return render_template("incident_form.html", user=current_user)


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