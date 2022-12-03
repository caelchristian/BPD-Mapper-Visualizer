from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
from .auth import get_strong_password

views = Blueprint('home', __name__)
suggest_password_bp = Blueprint('spw', __name__)
form_bp = Blueprint('form', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/suggest_password/', methods=['GET', 'POST'])
def get_password():
    print("Suggested Password: " + str(get_strong_password))
    return render_template("auth.html", user=current_user)

@views.route('/form', methods=['GET', 'POST'])
def form():
    return render_template("form.html", user=current_user)