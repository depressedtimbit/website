from ast import Num
from flask import Flask, render_template
from Flask_Migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth

    import getpass
    print(getpass.getuser())
    @app.errorhandler(404)
    def not_found(e):
      return render_template("404.html")

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

    def load_posts(User : Num = None):
        if User is None:
            return Post.query.all()
        else:
            return Post.query.filter_by(user_id=User)

    def load_pfp_dir(id : Num):
        user = User.query.get(int(id))
        if user.pfp == None:
            return "\static\pfps\default-pfp.png"
        else:
            return f'\static\pfps\custom\{user.pfp}'

            
    app.jinja_env.globals.update(load_posts=load_posts, load_user=load_user, load_pfp_dir=load_pfp_dir, len=len)


    return app


def create_database(app):
    print('Testing if Database exists')
    if not path.exists('/var/www/website/website' + DB_NAME):
        print('attemping to create Database')
        db.create_all(app=app)
        print('Created Database!')