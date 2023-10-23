from flask import Flask, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
import os 
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv('config.env')

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
cache = Cache()
cors = CORS()


DB_NAME = os.getenv("ENV_WEBSITE_DB_NAME")
DOMAIN = os.getenv("ENV_WEBSITE_DOMAIN")
SECRET_KEY = os.getenv("ENV_WEBSITE_SECRET_KEY")



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300
    app.config['SERVER_NAME'] = DOMAIN
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    cors.init_app(app)

    from .views import views
    from .auth import auth
    from .api1 import api

    # TODO: move to somewhere outside
    @app.errorhandler(404)
    def not_found(e):
      return render_template("404.html")

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/v1')

   

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .utils import load_user

    login_manager.user_loader(load_user)
    


    return app


def create_database(app):
    print('Testing if Database exists')
    DB_DIR = os.path.join(os.path.dirname(__file__), DB_NAME)
    #if not os.path.exists(DB_DIR):
    print('attemping to create Database')
    db.create_all(app=app)
    print('Created Database!')
