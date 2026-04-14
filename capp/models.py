from capp import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database User
class User(db.Model, UserMixin):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    transports = db.relationship('Transport', backref='author', lazy=True)

# Database Transport
class Transport(db.Model):
    __tablename__= 'transport_table'

    id = db.Column(db.Integer, primary_key=True)

    user_type = db.Column(db.String(20), nullable=False)
    transport = db.Column(db.String(50), nullable=False)

    kms = db.Column(db.Float, nullable=True)
    fuel = db.Column(db.String(50), nullable=True)

    flight_type = db.Column(db.String(50), nullable=True)
    cabin_class = db.Column(db.String(50), nullable=True)
    aircraft_type = db.Column(db.String(50), nullable=True)

    ferry_type = db.Column(db.String(50), nullable=True)
    train_type = db.Column(db.String(50), nullable=True)
    bicycle_type = db.Column(db.String(50), nullable=True)

    load = db.Column(db.Float, nullable=True)
    cargo_weight = db.Column(db.Float, nullable=True)

    volume = db.Column(db.Float, nullable=True)
    distance = db.Column(db.Float, nullable=True)
    energy_source = db.Column(db.String(50), nullable=True)

    co2 = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    