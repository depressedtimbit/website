from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.string(150), unique=True)
    password = db.Column(db.string(150))
    username =db.Column(db.string(150), unique=True)