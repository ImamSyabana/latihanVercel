from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import hashlib


db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()
bootstrap = Bootstrap()
login_manager = LoginManager()

def gravatar_url(email, size=100, default='retro', rating='g'):
    email = email.strip().lower().encode('utf-8')
    hash = hashlib.md5(email).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash}?s={size}&d={default}&r={rating}"

def create_app():
    app = Flask(__name__)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
    app.config.from_object(Config)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    app.jinja_env.globals['gravatar_url'] = gravatar_url

    #from app import routes, models

    # Setup console logging
    if not app.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask App startup')

    return app

@login_manager.user_loader
def load_user(id):
    if id:
        from app import models
        return db.session.get(models.User, int(id))
    return None