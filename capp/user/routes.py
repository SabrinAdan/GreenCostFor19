from flask import Flask, render_template, Blueprint, redirect, flash, url_for
from capp.user.forms import RegistrationForm

user = Blueprint('user', __name__)


@user.route('/register', methods=['GET', 'POST'])
def register_home():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Your account has been created! You can login now!',
              'success')
        return redirect(url_for('home.home_home'))
    return render_template('user/register.html', title='register', form=form)

@user.route('/login')
def login_home():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('You successfully logged in! You can count your emissions now!',
              'success')
        return redirect(url_for('home.home_home'))
    return render_template('user/login.html', title='login', form=form)