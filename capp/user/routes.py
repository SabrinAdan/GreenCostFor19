from capp import db, bcrypt
from flask import Flask, render_template, Blueprint, redirect, flash, request, url_for
from flask_login import current_user, login_user, logout_user
from capp.models import User
from capp.user.forms import LoginForm, RegistrationForm

user = Blueprint('user', __name__)


@user.route('/register', methods=['GET', 'POST'])
def register_home():
    form = RegistrationForm()
    
    if current_user.is_authenticated:
        return redirect(url_for('home.home_home')) 
    
    if form.validate_on_submit():
        user_hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        users = User(username=form.username.data, email=form.email.data, password=user_hashed_password)
        db.session.add(users)
        db.session.commit()
        flash('Your account has been created! You can login now!',
              'success')
        return redirect(url_for('home.home_home'))
    return render_template('user/register.html', title='register', form=form)


@user.route('/login', methods=['GET','POST'])
def login_home():
  form = LoginForm()
  if current_user.is_authenticated:
        return redirect(url_for('home.home_home'))
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user)
        next_page = request.args.get('next')
        flash('You have logged in! Now, you can start to use our Carbon App!', 'success')
        return redirect(next_page) if next_page else redirect(url_for('home.home_home'))
    else:
        flash('Login Unsuccessful. Please check email and password!', 'danger') 
  return render_template('user/login.html', title='login', form=form)

@user.route('/logout')
def logout():    
    logout_user()
    return redirect(url_for('home.home_home'))






