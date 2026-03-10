from flask import Flask, render_template, Blueprint

aboutUs = Blueprint('aboutUs', __name__)


@aboutUs.route('/aboutUs')
def aboutUs_home():
    return render_template('aboutUs.html', title='aboutUs')