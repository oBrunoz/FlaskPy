from flask import render_template, Blueprint, flash, url_for, redirect
from flask_login import login_required

admin_blueprints = Blueprint('admin', __name__, template_folder='templates')

@admin_blueprints.route('/admin')
@login_required
def admin():
    id = current_user.id

    if id == 9:
        return render_template('admin.html')
    else:
        flash('Você não tem autorização para acessar essa página!', 'error')
        return redirect(url_for('index'))