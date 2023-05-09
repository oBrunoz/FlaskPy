from flask import Flask
from app.routes.admin.adm import admin_blueprints
from flask_bootstrap import Bootstrap
from app.db.db import database
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='templates', static_folder='static')
app.register_blueprint(admin_blueprints)

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