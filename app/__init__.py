from flask import Flask, redirect, request, url_for
from app.routes.admin.adm import admin_blueprints
# from app.routes.admin import SecureModelView
from app.db.db import database
from app.models.User import User
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin

app = Flask(__name__, template_folder='templates', static_folder='static')

app.register_blueprint(admin_blueprints)
adminPage = Admin(app, template_mode='bootstrap4')

from app.models.Admin import Administrator
# adminPage.add_view(SecureModelView(Administrator, database.session))
# adminPage.add_view(SecureModelView(User, database.session))

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

Bootstrap(app)

app.config.from_object('config')

database.init_app(app)
migrate = Migrate(app, database)

# Admin view


#FLASK SECURITY


from app.routes import user 