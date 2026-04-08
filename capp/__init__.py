from flask import Flask
application = Flask(__name__)

application.config['SECRET_KEY'] = '7a567311e27e3eee2dffce8c23e7b2ae38774499e7373960'

from capp.home.routes import home
from capp.methodology.routes import methodology
from capp.carbon_app.routes import carbon_app
from capp.aboutUs.routes import aboutUs
from capp.user.routes import user

application.register_blueprint(home)
application.register_blueprint(methodology)
application.register_blueprint(carbon_app)
application.register_blueprint(aboutUs)
application.register_blueprint(user)