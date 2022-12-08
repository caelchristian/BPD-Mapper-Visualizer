from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    db.init_app(app)
    

    # from .views import home_bp, auth_bp, form_bp, suggest_password_bp
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Incidents, Arrests

    # get the user's session in the db
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    if not os.path.exists("instance/data.db"):
        with app.app_context():
            db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def get_db_connection():
  conn = sqlite3.connect('instance/data.db')
#   conn.row_factory = sqlite3.Row
  return conn

    
def show_plots():
  import pandas as pd
  import matplotlib.pyplot as plt
  from matplotlib import rcParams
  from . import get_db_connection

  conn = get_db_connection()
  rcParams.update({'figure.autolayout': True})

  # # OCCURANCES / ARREST CATEGORY
  query = f"""SELECT category, COUNT(category)
              FROM (incidents i JOIN arrests a
              ON a.incident_number = i.incident_number)
              GROUP BY category;
              """
                      
  df = pd.read_sql_query(query,conn)

  # render plot from dataframe
  df.plot.bar(x = "category",
          y = "COUNT(category)")
  
  plt.title("Occurances per Arrest Category in 2021")
  
  plt.show()
  
  
    # # OCCURANCES / ARREST CATEGORY
  query = f"""SELECT call_type, COUNT(call_type)
              FROM (incidents i JOIN arrests a
              ON a.incident_number = i.incident_number)
              GROUP BY call_type;
              """
                      
  df = pd.read_sql_query(query,conn)
  
  df = df[df["COUNT(call_type)"] > 10]

  # render plot from dataframe
  df.plot.bar(x = "call_type",
          y = "COUNT(call_type)")
  
  plt.title("Arrests with >30 Occurances in 2021")
  
  plt.show()
  
  
  
  # IGNORE (I tried plotting with datetime but it turns out it's hard)
  
  
  # query = f"""SELECT category, COUNT(category)
  #             FROM (incidents i JOIN arrests a
  #             ON a.incident_number = i.incident_number)
  #             GROUP BY category;
  #             """
                      
  # df = pd.read_sql_query(query,conn)
  
  # import numpy as np
  
  # df = df[["arrest_date","felony"]]
  
  # df['arrest_date'] = pd.to_datetime(df["arrest_date"])

  # # sort dates
  # # s = df['arrest_date'].value_counts().sort_index()
  
  # df.groupby([df["arrest_date"], 'felony']).count().plot(kind='bar')
  
  # # df.plot(x = "arrest_date",
  # #         y = "most_serious",
  # #         kind="scatter")
  
  # plt.show()
  
  # occurances for each charge
  # query = f"""
  #         SELECT count()
  #          """
  
  # plt.plot(df['arrest_date'],df[])

  # render plot from dataframe
  # df.plot.pie(
  #         x = "category",
  #         y = "COUNT(category)")
  