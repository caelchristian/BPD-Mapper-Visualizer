from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from base64 import b64encode
import os
from pathlib import Path
from random import sample, choice
import sqlalchemy

# special characters

CHARACTERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
              'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
              'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
              'z' 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
             'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
             'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y','Z',
             '@', '#', '$', '%', '=', ':', ';', '?', '!',
             '&', '\'', '-''.', '/', '|', '~', '>', '*',
             '(', ')', '<', '[', ']', '^', '_', '`', '{',
             '|' '}', '~']


SPECIAL_CHARS = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
NUMBERS = "1234567890"

auth_bp = Blueprint('auth', __name__)


# UserMixin is required for Flask-Login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    salt = db.Column(db.String(150))
    access = db.Column(db.String(5))
    attempts = db.Column(db.Integer)


def get_strong_password(CHARACTERS, length):
    no_special_chars = True
    password = ""
    while no_special_chars:
        password = ''.join(choice(CHARACTERS) for x in range(length))
        for char in password:
            if char in password:
                no_special_chars = False
                
    return password


@auth_bp.route('/auth', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        try:

            if 'spw' in request.form and request.form['spw'] == 'suggest':
                flash('Strong password: ' + str(get_strong_password(CHARACTERS, 25)), category='success')

            # if user requests to log in
            elif 'button' in request.form and request.form['button']== 'login':

                email = request.form.get('email-login')
                password = request.form.get('password-login')

                # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
                user = User.query.filter_by(email=email).first()
                

                if user:
                    if user.attempts > 1:
                        # Check if the password matches the hash
                        if check_password_hash(user.password, password):
                            flash('Logged in successfully!', category='success')
                            login_user(user, remember=True)
                            # update attempts back to 3
                            user.attempts = 3
                            db.session.commit()
                            return redirect(url_for('home.home'))
                        else:
                            user.attempts -= 1
                            db.session.commit()
                            flash('Wrong password, you have ' + str(user.attempts) + ' password attempt(s) remaining.',
                                    category='error')
                    else:
                        # Lock out user if 0 attempts
                        flash('This account has 0 password attempts remaining. Please contact an administrator.',
                                category='error')
                        return redirect(url_for('home.home'))
                else:
                    flash('The email address provided has not been registered.', category='error')

            # user attempts to sign up
            elif 'button' in request.form and request.form['button'] == 'signup':

                email = request.form.get('email-signup')
                password = request.form.get('password-signup')

                # salt should be same length as output of hash (32 bytes)
                salt = b64encode(os.urandom(32)).decode('utf-8')

                # search for email in db, if it exists
                if User.query.filter_by(email=email).first():
                    flash('Email address provided already exists.', category='error')
                elif len(email) < 6:
                    flash('Email address must be at least 3 characters.', category='error')
                elif len(password) < 7:
                    flash('Password must be at least 8 characters.', category='error')
                elif len(password) > 25:
                    flash('Password cannot be longer than 25 characters.', category='error')
                elif not any(char.isupper() for char in password):
                    flash('Password must contain at least one uppercase character.', category='error')
                elif not any(char.islower() for char in password):
                    flash('Password must contain at least one lowercase character.', category='error')
                # if password doesn't contain any special characters, flash
                elif not any((char in SPECIAL_CHARS) for char in password):
                    flash('Password must contain at least one special character.', category='error')
                elif not any((num in NUMBERS) for num in password):
                    flash('Password must contain at least one number.', category='error')
                else:
                    # password is hashed 150,000 iterations with sha1
                    password = generate_password_hash(password, method="sha1")

                    # create the user in the database and commit changes
                    new_user = User(email=email, password=password, salt=salt, access='pleb', attempts='3')
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user, remember=True)
                    
                    # create a folder for user for storing generated images if folder doesn't exist already
                    if not os.path.isdir(f'final/static/{new_user.id}/'):
                        os.makedirs(f'final/static/{new_user.id}')
                    

                    # return to home
                    flash('Account created!', category='success')
                    return redirect(url_for('home.home'))
        except sqlalchemy.exc.OperationalError as e:
            flash(sqlalchemy.exc.OperationalError, e)

    return render_template("auth.html", user=current_user)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
