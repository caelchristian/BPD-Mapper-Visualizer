from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path, environ
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
    
    if not path.exists("instance/data.db"):
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