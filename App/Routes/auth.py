from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from App.Database.Models.User import User
from App.Module.Form.login import LoginForm


r_auth = Blueprint('auth', __name__)


@r_auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        login_post(form)
    return render_template('security/login_user.html')


def login_post(form):
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        flask.flash('Logged in successfully.')

        return redirect(url_for('main.profile'))


@r_auth.route('/signup', methods=['POST'])
def signup():
    # code to validate and add user to database goes here
    return redirect(url_for('auth.login'))
