from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
from .auth import get_strong_password
from .models import User, Arrest, Incident

views = Blueprint('home', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/suggest_password/', methods=['GET', 'POST'])
def get_password():
    print("Suggested Password: " + str(get_strong_password))
    return render_template("auth.html", user=current_user)


@views.route('/form', methods=['GET', 'POST'])
def form():
    dict = {}
    if request.method == 'POST':
        if 'incident_button' in request.form:
            f = request.form
            for key in f.keys():
                for value in f.getlist(key):
                    dict[key] = value
                 
        Incident(
        objectid = dict["objectid"],
        incident_number = dict["incident_number"],
        arrest_date = dict["arrest_date"],
        gender = dict["gender"],
        race = dict["race"],
        age = dict["age"],
        charge = dict["charge"],
        most_serious = dict["most_serious"],
        felony = dict["felony"],
        violent = dict["violent"],
        category = dict["category"]
        )
        
        # insert into database
        db.session.add()
        db.session.commit()
                    
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

            
            
            
                
    return render_template("form.html", user=current_user)