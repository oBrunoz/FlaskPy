from flask import render_template, Blueprint, flash, url_for, redirect, session
from flask_login import login_required, current_user
from app.models.Admin import Administrator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError
from app.routes.admin import admin_manager

admin_blueprints = Blueprint('adm', __name__, template_folder='templates')

@admin_manager.user_loader
def load_admin(id):
    return Administrator.query.get(int(id))

class LoginAdminForm(FlaskForm):
    admUser = StringField('admUser', validators=[DataRequired()])
    admSenha = PasswordField('admSenha', validators=[InputRequired(), Length(min=8, max=30)])

@admin_blueprints.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginAdminForm()

    from app import bcrypt
    if form.validate_on_submit():
        admUser = Administrator.query.filter_by(nome=form.admUser.data).first()
        if admUser:
            if bcrypt.check_password_hash(admUser.senha, form.admSenha.data):
                session['logged_in'] = True
                flash('Conectado com sucesso!', 'success')
                return redirect(url_for('admin_loged'))
            else:
                flash('Usuário ou senha incorretos!', 'error')
        else:
            flash('Usuário ou senha incorretos!', 'error')

    return render_template('admin.html', form=form)

# CORRIGIR ERRO DE REDIRECIONAMENTO PARA ADMIN_LOGED()

@admin_blueprints.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_loged():
    if session['logged_in'] == True:
        return render_template('index.html')

@admin_blueprints.route('/admin/logout', methods=['GET', 'POST'])
def adm_logout():
    session.clear()
    flash('Admin Deslogado!', 'success')
    return redirect('/')
