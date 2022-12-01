from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///credentials.db'
    db.init_app(app)
    

    from .views import home_bp
    from .auth import auth_bp
    from .views import suggest_password_bp
    from .views import form_bp

    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(suggest_password_bp, url_prefix='/')
    app.register_blueprint(form_bp, url_prefix='/')
    
    from .auth import User

    # get the user's session in the db
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

