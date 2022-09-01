from sqlalchemy import func
from . import db
from flask_login import UserMixin



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    posts = db.relationship('Post')
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    pfp = db.Column(db.String(150), nullable=True)
    bio = db.Column(db.String(150), nullable=True)
