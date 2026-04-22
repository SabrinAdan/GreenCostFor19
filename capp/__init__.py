from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os


db = SQLAlchemy()
login_manager = LoginManager()


application = Flask(__name__)


application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','dev-secret-key')
#application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
#application.config['SQLALCHEMY_BINDS'] ={'transport': 'sqlite:///transport.db'}
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(application)
bcrypt = Bcrypt(application)
login_manager.init_app(application)
login_manager.login_view = 'user.login_home'
login_manager.login_message_category = 'info'


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
