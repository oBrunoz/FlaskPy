from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from app.db.db import database
from flask_migrate import Migrate
from app.routes.user import bpUser

app = Flask(__name__, template_folder='flask/app/templates', static_folder='app/static')
Bootstrap(app)

connection = 'sqlite:///meubanco.db'

app.config['SECRET_KEY'] = 'senhasecreta' #chave secreta de cookie
app.config['SQLALCHEMY_DATABASE_URI'] = connection
app.config['SQLALCHEMY_TRACKMODIFICATIONS'] = False
app.register_blueprint(bpUser, url_prefix='/')

database.init_app(app)
migrate = Migrate(app, database)

@app.route('/')
def index():
    return redirect(url_for('bpUser.index'))

if __name__ == "__main__":
    app.run(debug=True)
