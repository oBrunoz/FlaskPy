from flask import Flask
from flask_bootstrap import Bootstrap
from app.db.db import database
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, login_required, logout_user
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='templates', static_folder='static')
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

Bootstrap(app)

connection = 'sqlite:///meubanco.db'

app.config.from_object('config')

database.init_app(app)
migrate = Migrate(app, database)

from app.routes import user 