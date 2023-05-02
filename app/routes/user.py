from flask import Blueprint, render_template, request, redirect
from app.models import User
from app.db.db import database as db

bpUser = Blueprint('bpUser', __name__, url_prefix='/', template_folder='../templates')

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
                errors.append('Por favor, insira seu nome.')

            if not senha or type(senha) != str or len(senha) <= 8:
                errors.append('Por favor, insira a senha corretamente')

            if senha != confirmSenha:
                errors.append('Senhas incorretas!')
            
            if len(errors) > 0:
                return render_template('userCreate.html', errors=errors)

            else:
                user = User.User(nome, email, senha)
                db.session.add(user)
                db.session.commit()
                return redirect('/cadastro')
            
        except SyntaxError:
            return 'Sla'

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
        user = request.form.get('usuario')
        senha = request.form.get('senha')
        if user != 'admin':
            return 'Usuário \'{}\' errado!'.format(user)
        if senha != '123456':
            return 'Senha \'{}\' errada!'.format(senha)
        else:
            return 'Parabéns!'

@bpUser.route('/create/adm')
def adm():
    return render_template('contatos.html')
