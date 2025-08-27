from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_gravatar import Gravatar

db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()
bootstrap = Bootstrap5()
login_manager = LoginManager()

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

    # create gravatar 
    gravatar = Gravatar(app,
                        size=100,
                        rating='g',
                        default='retro',
                        force_default=False,
                        force_lower=False,
                        use_ssl=False,
                        base_url=None)
    
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