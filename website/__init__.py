from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Post

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def load_post(id):
        return Post.query.get(int(id))

    def load_posts():
        return Post.query.all()

    app.jinja_env.globals.update(load_posts=load_posts, load_user=load_user)


    return app


def create_database(app):
    print('Testing if Database exists')
    if not path.exists('website/' + DB_NAME):
        print('attemping to create Database')
        db.create_all(app=app)
        print('Created Database!')