from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import get_db_connection
from sqlalchemy import insert, create_engine
# from sqlalchemy.orm import Session
from .auth import get_strong_password
# from .models import User, Arrests, Incidents
import os

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
    modify = False
    objectid = None
    incident_number = None
    
    if request.method == 'POST':
        conn = get_db_connection()
        # User chooses to create new entry
        if request.form.get("modify") == "on":
            # user chose to modify a record
            modify = True
            # retrieve id
            objectid = request.form.get("objectid")
            if objectid:
                # try to find record from objectid
                res = conn.execute(f"""SELECT * 
                                    FROM incidents
                                    WHERE objectid = {objectid}
                                    """)
                
                # if record exists
                if res.fetchone():
                    # grab incident_number
                    res = conn.execute(f"""SELECT incident_number 
                                    FROM incidents
                                    WHERE objectid = {objectid}
                                    """)
                    
                    incident_number = res.fetchone()[0]
                    
                    # attempt to change column of record
                    conn.execute(f"""
                                    DELETE FROM incidents
                                    WHERE objectid = {objectid}
                                    """)
                else:
                    flash(f"Record could not be found with objectid = {objectid}", category="error")
                    print("record not found")
            else:
                flash(f"Object ID must be specified for modifying existing entries.", category="error")
        
        any_none_values = False
        for key, val in request.form.items():
            print(key,":",val)
            # unchecked buttons are not keys in dict
            # exclude submit button
            if val == "" and key not in ["button","objectid"]:
                any_none_values = True
                    
        if not any_none_values:
            # don't overwrite unique fields if modifying
            if not modify:            
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
                
            areaname = request.form.get("areaname")
            latitude = request.form.get("latitude")
            longitude = request.form.get("longitude")
            district = request.form.get("district")
            priority = request.form.get("priority")
            
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
        print("got here")
                
    return render_template("incident_form.html", user=current_user)


@views.route('/arrest_form', methods=['GET', 'POST'])
def arrest_form():
    table_name = "arrests"
    modify = False
    
    # Column names
    objectid = None
    incident_number = None
    
    if request.method == 'POST':
        conn = get_db_connection()
        # User chooses to create new entry
        if request.form.get("modify") == "on":
            # user chose to modify a record
            modify = True
            # retrieve id
            objectid = request.form.get("objectid")
            if objectid:
                # try to find record from objectid
                res = conn.execute(f"""SELECT * 
                                    FROM arrests
                                    WHERE objectid = {objectid}
                                    """)
                # if record exists
                if res.fetchone():
                    # grab incident_number
                    res = conn.execute(f"""SELECT incident_number 
                                    FROM incidents
                                    WHERE objectid = {objectid}
                                    """)
                    
                    incident_number = res.fetchone()[0]
                    
                    # attempt to change column of record
                    conn.execute(f"""
                                    DELETE FROM arrests
                                    WHERE objectid = {objectid}
                                    """)
                else:
                    flash(f"Record could not be found with objectid = {objectid}", category="error")
                    print("record not found")
            else:
                flash(f"Object ID must be specified for modifying existing entries.", category="error")
                
        any_none_values = False
        for key, val in request.form.items():
            # unchecked buttons are not keys in dict
            # exclude submit button
            print(key,":",val)
            if val == "" and key not in ["button","objectid"]:
                any_none_values = True
                    
        if not any_none_values:
            # don't overwrite objectid if modifying
            if not modify:
                res = conn.execute(f"""
                    SELECT MAX(objectid) FROM {table_name}
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
                (objectid, incident_number, arrest_date, gender, race, age,
                 charge, most_serious, felony, violent, category))
            conn.commit()
            
            flash("Successfully inserted into table!", category="info")
        else:
            flash("One or more text box values are either empty or invalid", category="error")
            
    return render_template("arrest_form.html", user=current_user)

@views.route('/delete', methods=['GET', 'POST'])
def delete_record():
    if request.method == "POST":
        objectid = request.form.get("objectid")
        if objectid:
            table = request.form.get("table")
            confirm = request.form.get("confirm")
            if confirm:
                # valid query
                conn = get_db_connection()
                res = conn.execute(f"""
                                    DELETE FROM {table}
                                    WHERE objectid = {objectid}
                                    """)
                conn.commit()
                flash("Successfully deleted record.", category="info")
            else:
                flash("Please confirm by checking the box.")
        else:
            flash("Enter the Object ID of the record you would like to delete.", category="error")
            
    return render_template("delete.html", user=current_user)

@views.route("/stat_query", methods=['GET','POST'])
def stat_query():
    if request.method == "POST":
        import statistics
        result = None
        column_list = []
        
        col = request.form.get("column")
        op = request.form.get("operation")
        conn = get_db_connection()
        
        # # if query involves objectid or incident_number
        if col in ["incident_number", "objectid"]:
            # specify table to avoid ambigious column name
            col = "i." + col
            
        # if sql can do operation, just execute query dynamically
        if op in ["min", "max", "sum"]:
            res = conn.execute(f"""SELECT {op}({col})
                         FROM (incidents i JOIN arrests a
                               ON a.incident_number = i.incident_number);
                         """)
            
            result = res.fetchone()[0]
        # otherwise get the column and insert into list
        else:
            print(f"""SELECT {col}
                         FROM (incidents i JOIN arrests a
                               ON a.incident_number = i.incident_number);
                         """)
            res = conn.execute(f"""SELECT {col}
                         FROM (incidents i JOIN arrests a
                               ON a.incident_number = i.incident_number);
                         """)
            
            for row in res.fetchall():
                column_list.append(row[0])
                print(row[0])
                
            if op == "mean":
                result = statistics.mean(column_list)
            elif op == "median":
                result = statistics.median(column_list)
            elif op == "std mean":
                result = statistics.stdev(column_list)
            elif op == "count":
                result = len(column_list)
                
    
        return render_template("stat_query.html", result=str(result), user=current_user)
    else:
        return render_template("stat_query.html", user=current_user)

@views.route("/cond_query", methods=['GET','POST'])
def cond_query():
    if request.method == "POST":
        import pandas as pd
        result = None
        df = pd.DataFrame()
        query = ""
        table = None
        conn = get_db_connection()
    
        # specify table to avoid ambigious column name
        col = "" + request.form.get("column")    
        cond = request.form.get("condition")
        inpt = request.form.get("input")
        order = request.form.get("order")
        
        # avoid ambiguious columns
        if col in ["objectid","incident_number"]:
            col = "i." + col

        if order != "*":
            query = f"""SELECT {col}
                        FROM (incidents i JOIN arrests a
                        ON a.incident_number = i.incident_number)
                        WHERE {cond} = {inpt}
                        ORDER BY {order};
                        """
        else:
            query = f"""SELECT {col}
                        FROM (incidents i JOIN arrests a
                        ON a.incident_number = i.incident_number)
                        WHERE {cond} = {inpt};
                        """
        try:
            # too easy bruh
            df = pd.read_sql_query(query,conn)
            table = df.to_html(classes="center table table-sm table-dark")
        except:
            flash("There was an error executing SQL. Please check your inputs and try again.", category="error")

        return render_template("cond_query.html", df=df, table=table, user=current_user)

    else:
        return render_template("cond_query.html", user=current_user)