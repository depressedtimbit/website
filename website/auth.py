import re
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    return render_template("login.html", bool=True)

@auth.route('/logout')
def logout():
    return "<p>logout function<p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email not valid', category='error')
        elif len(username) < 2:
            flash('username must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\' match', category='error')
        elif len(password1) <7:
            flash('Password must be greater than 6 character', category='error')
        else:
            flash('Account created', category='success')
            #add user
    return render_template("sign_up.html")