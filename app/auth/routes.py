from flask import Blueprint, flash, redirect, render_template, request, url_for
from .forms import LoginForm, SignUpForm
from ..models import User
from flask_login import current_user,login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from email_validator import validate_email

auth = Blueprint('auth', __name__, template_folder='auth_templates')

# @auth.route('/')
# def home_page():
#     return render_template('index.html')

@auth.route('/signup', methods=["GET", "POST"])
def signup_page():
    form = SignUpForm()
    
    if request.method == 'POST':
        if form.validate():
            first_name = form.first_name.data.title().strip()
            last_name = form.last_name.data.title().strip()
            username = form.username.data.strip()
            email = form.email.data.strip()
            password = form.password.data

            is_new_account = True

            if first_name == "" or last_name == "" or username == "":
                flash('You must enter something for every field. Spaces are not accepted as valid entries', 'danger')
                return render_template('signup.html', form = form)

            # Make sure the user is not in the db yet
            try:
                validation = validate_email(email, check_deliverability=is_new_account)
                email = validation.email
            except: 
                #invalid email
                flash("The email you are trying to submit is not a properly formatted email.", "danger")
                return render_template('signup.html', form = form)
            
            email_already_exists = User.query.filter_by(email=email).first()
            if not email_already_exists:
                username_already_exists = User.query.filter_by(username=username).first()
                if username_already_exists:
                    flash("That username is taken. Please choose a different username.", "danger")
                else:
                    user = User(first_name, last_name, username, email, password)
                    user.save_to_db() 
                    login_user(user)
                    return redirect(url_for('home_page'))
            else:
                flash('A user with that email already exists. Try entering a new email, or logging in.', "danger")
    
    # if password does not equal confirm password data:
    if form.password.data != form.confirm_password.data:
        flash("The password you entered was not correctly confirmed. Please make sure you type the same password twice.", "danger")      

    return render_template('signup.html', form = form)

@auth.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()            
            if user:
                # verify password
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('home_page'))
                else:
                    flash('Incorrect username or password. Please try again.', 'danger')
            else:
                flash('Incorrect username or password. Please try again.', 'danger')


    return render_template('login.html', form = form)

@auth.route('/logout')
@login_required
def log_me_out():
    logout_user()
    return redirect(url_for('auth.login_page'))
