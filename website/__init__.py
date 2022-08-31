from typing import Optional
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()
cache = Cache()
socketio = SocketIO()

website_url = 'checkhost.local:5000'

def Create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300
    app.config['SERVER_NAME'] = website_url
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    socketio.init_app(app)

    from .views import views
    from .auth import auth
    from .api1 import api
    from .knucklebones import bones

    # TODO: move to somewhere outside
    @app.errorhandler(404)
    def not_found(e):
      return render_template("404.html")

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/v1')
    app.register_blueprint(bones, url_prefix="/knucklebones")

    from .models import User, Post

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id_):
        return User.query.get(int(id_))

    # FIXME: unused view?
    def load_post(id_):
        return Post.query.get(int(id_))

    def load_posts(user: Optional[int]):
        if user is None:
            return Post.query.all()
        else:
            return Post.query.filter_by(user_id=user)

    def load_pfp_dir(id_):
        user = User.query.get(int(id_))
        if user.pfp == None:
            return "/static/pfps/default-pfp.png"
        else:
            return f'/static/pfps/custom/{user.pfp}'

    app.jinja_env.globals.update(load_posts=load_posts, load_user=load_user, load_pfp_dir=load_pfp_dir, len=len)

    return app


def create_database(app):
    print('Testing if Database exists')
    if not path.exists('/var/www/website/website' + DB_NAME):
        print('attemping to create Database')
        db.create_all(app=app)
        print('Created Database!')
