from flask import Flask, render_template, Blueprint

user = Blueprint('user', __name__)

@user.route('/user')
def user_home():
  return render_template('user.html', title='user')

@user.route('/register')
def register_home():
    return render_template('register.html')

@user.route('/login')
def login_home():
    return render_template('login.html')