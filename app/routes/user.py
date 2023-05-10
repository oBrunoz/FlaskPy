from app import app, bcrypt, login_manager
from app.models.User import User
from app.db.db import database as db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError

@login_manager.user_loader
def load_user(userId):
    return User.query.get(int(userId))

class CadastroForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[InputRequired(), Length(min=8, max=30)])
    confirmSenha = PasswordField('confirmSenha', validators=[InputRequired()])

    def validateEmail(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            flash('Email existente', 'error')
        
    def validate_username(self, name):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        existing_user = User.query.filter_by(nome=name.data).first()
        if existing_user:
            raise ValidationError(f'User {name.data} is already used.')
        for char in self.name.data:
            if char in excluded_chars:
                flash(f"Character {char} is not allowed in username.", 'error')
                raise ValidationError(
                    f"Character {char} is not allowed in username.")
        
class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[InputRequired(), Length(min=8, max=30)])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(nome=form.name.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, form.senha.data):
                login_user(user)
                return redirect(url_for('loged'))
            else:
                flash('Senha incorreta!', 'error')
        else:
            flash('Usuário não existe, tente novamente.', 'error')

    return render_template('base.html', form=form)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    try:
        if form.validate_on_submit():
            if form.senha.data != form.confirmSenha.data:
                print('Senhas erradas') 
                raise ValidationError('Senhas incorretas!')
                #Faço alguma coisa futuramente
            if form.validateEmail(form.email) and form.validate_username(form.name):
                flash('Erro', 'error')
            else:
                hashed_password = bcrypt.generate_password_hash(form.senha.data)
                newUser = User(nome=form.name.data, email=form.email.data, senha=hashed_password)
                db.session.add(newUser)
                db.session.commit()
                return redirect(url_for('login'))

        return render_template('userCreate.html', form=form)
    except Exception as err:
        raise('Houve um erro.', err)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(nome=form.name.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, form.senha.data):
                login_user(user)
                flash('Logado!', 'success')
                return redirect(url_for('loged'))
            else:
                flash('Senha incorreta!', 'error')
        else:
            flash('Usuário não existe, tente novamente.', 'error')

    return render_template('login.html', form=form)
    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def upt(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        try:
            user.nome = nome
            user.email = email
            db.session.add(user)
            db.session.commit()
            flash(f'ID {id} editado com sucesso!', 'success')
            return redirect(url_for('contato'))
        except:
            flash('Houve um erro ao editar usuário, tente novamente.', 'error')
            return redirect(url_for('contato'))
    else:
        return render_template('userUpdate.html', user=user)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    user = User.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('userDelete.html', user=user)
    if request.method == 'POST':
        try:
            db.session.delete(user)
            db.session.commit()
            flash(f'ID {id} deletado!', 'error')
            return redirect(url_for('contato'))
        except:
            flash('Houve um erro ao deletar o usuário, tente novamente.')
            return redirect(url_for('contato'))

@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def loged():
    return render_template('loged.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Deslogado!', 'success')
    return redirect(url_for('index'))

@app.route('/contatos')
@login_required
def contato():
    users = User.query.all()
    return render_template('contatos.html', users=users)
