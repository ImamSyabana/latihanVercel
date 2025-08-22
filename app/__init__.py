from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from flask_ckeditor import CKEditor

from flask_bootstrap import Bootstrap5
from flask_login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config.from_object(Config)
ckeditor = CKEditor(app)
Bootstrap5(app)


# TODO: Configure Flask-Login
# initiate login manager object
login_manager = LoginManager()
# conect login manager dengan app
login_manager.init_app(app)

#Set the login view: Flask-Login will redirect unauthenticated users to this route.
login_manager.login_view = "login"


from app import routes, models

@login_manager.user_loader
def load_user(id):
    if id:
        # This function MUST exist and return a user object or None
        return db.get_or_404(models.User, int(id))
    return None

db = SQLAlchemy(app)
migrate = Migrate(app, db)



# Setup console logging
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Flask App startup')