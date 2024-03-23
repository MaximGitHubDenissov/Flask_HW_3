from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25), unique=False, nullable=False)
    user_last_name = db.Column(db.String(25), unique=False, nullable=False)
    user_password = db.Column(db.String(12), unique=False, nullable=False)
    user_email = db.Column(db.String(25), unique=True, nullable=False)
