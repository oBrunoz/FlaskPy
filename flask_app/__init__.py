from flask import Flask, redirect, request, url_for, session, abort, render_template
from flask_app.routes.admin.adm import admin_blueprints
from flask_app.db.db import database as db
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin 

app = Flask(__name__, template_folder='templates', static_folder='static')

app.register_blueprint(admin_blueprints)
adminPage = Admin(app, template_mode='bootstrap4')


bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

Bootstrap(app)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)

class SecureModelView(ModelView):
    def is_accessible(self):
        if 'logged_in' in session:
            return True
        else:
            print('DEU NAO OTARIO')
            abort(403)

    def handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return render_template('403.html'), 403
            # Arrumar abort page

from flask_app.models.Admin import Administrator
from flask_app.models.User import User

adminPage.add_view(SecureModelView(Administrator, db.session))
adminPage.add_view(SecureModelView(User, db.session))


from flask_app.routes import user 