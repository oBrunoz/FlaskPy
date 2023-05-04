from flask import Blueprint, render_template, request, redirect, Flask, url_for, flash
from app.models import User
from app.db.db import database as db
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)
bpUser = Blueprint('bpUser', __name__, url_prefix='/', template_folder='../templates')
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def login_user(userId):
    return User.User.query.get(str(userId))

@bpUser.route('/')
def index():
    return render_template('base.html')

@bpUser.route('/cadastro', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('userCreate.html')
    if request.method == 'POST':
        try:
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')
            confirmSenha = request.form.get('confirmSenha')
            errors = [];

            if not nome or type(nome) != str:
                flash('Por favor, insira seu nome.', 'error')
                errors.append(1)

            if not senha or type(senha) != str:
                flash('Por favor, insira a senha corretamente', 'error')
                errors.append(1)

            if not senha == 'admin':
                flash('Por favor, insira a senha corretamente', 'error')
                errors.append(1)

            if senha != confirmSenha:
                flash('Senhas incorretas!', 'error')
                errors.append(1)
            
            if len(errors) > 0:
                return render_template('userCreate.html')

            if nome and email and senha and confirmSenha:
                existing_email = User.User.query.filter_by(email=email).first()
                existing_nome = User.User.query.filter_by(nome=nome).first()
                if existing_email:
                    raise ValidationError('That email already exists. Please choose a different one.')
                if existing_nome:
                    raise ValidationError('That name already exists. Please choose a different one.')
                else:
                    hashed_password = bcrypt.generate_password_hash(senha)
                    user = User.User(nome, email, hashed_password)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('bpUser.login'))
            
            return render_template('userCreate.html')
        except Exception as e:
            raise e

@bpUser.route('/dados')
def recovery():
    users = User.User.query.all()
    return render_template('userRecovery.html', users=users)

@bpUser.route('/update/<int:id>', methods=['GET', 'POST'])
def upt(id):
    user = User.User.query.get(id)

    if request.method == 'GET':
        return render_template('userUpdate.html', user=user)
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')

        user.nome = nome
        user.email = email
        db.session.add(user)
        db.session.commit()
        return redirect('/dados')

@bpUser.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user = User.User.query.get(id)

    if request.method == 'GET':
        return render_template('userDelete.html', user=user)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect('/dados')

@bpUser.route('/contatos')
def contato():
    users = User.User.query.all()
    return render_template('contatos.html', users=users)

@bpUser.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        nome = request.form.get('usuario')
        senha = request.form.get('senha')

        if nome and senha:
            validadeUser = User.User.query.filter_by(nome=nome).first()
            if validadeUser:
                if bcrypt.check_password_hash(validadeUser.senha, senha):
                    login_user(validadeUser)
                    return redirect(url_for('bpUser.loged'))
        
        flash('Não foi possível fazer login!', 'error')
        return render_template('login.html')
    
@bpUser.route('/dashboard', methods=['POST', 'GET'])
@login_required
def loged():
    return render_template('loged.html')
    
@bpUser.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@bpUser.route('/create/adm')
def adm():
    return render_template('contatos.html')
