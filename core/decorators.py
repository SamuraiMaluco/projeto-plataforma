from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor, faça login para acessar essa página', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_functions(*args, **kwargs):
        if not current_user.is_admin:
            flash ('Acesso restrito a administradores', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_functions(*args, **kwargs):
        if not current_user.is_admin:
            flash('Acesso restritio a administrador ', 'danger')
            return redirect(url_for('core.home'))
            