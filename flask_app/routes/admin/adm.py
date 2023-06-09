from flask import render_template, Blueprint, flash, url_for, redirect, session, request
from flask_login import login_required, current_user
from flask_app.models.Admin import Administrator
from flask_app.db.db import database as db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError

admin_blueprints = Blueprint('adm', __name__, template_folder='templates')

class LoginAdminForm(FlaskForm):
    admUser = StringField('admUser', validators=[DataRequired()])
    admSenha = PasswordField('admSenha', validators=[InputRequired(), Length(min=8, max=30)])

@admin_blueprints.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginAdminForm()

    from flask_app import bcrypt
    if form.validate_on_submit():
        admUser = Administrator.query.filter_by(nome=form.admUser.data).first()
        if admUser:
            if bcrypt.check_password_hash(admUser.senha, form.admSenha.data):
                session['logged_in'] = True
                flash('Conectado com sucesso!', 'success')
                return redirect('/admin')
            else:
                print('Senha ou usuario errados!')
                flash('Usuário ou senha incorretos!', 'error')
        else:
            print('Algo errado')
            flash('Usuário ou senha incorretos!', 'error')

    return render_template('adm_templates/admin_login.html', form=form)

@admin_blueprints.route('/admin/logout')
def adm_logout():
    session.clear()
    flash('Admin Deslogado!', 'success')
    return redirect('/')
