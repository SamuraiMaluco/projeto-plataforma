from functools import wraps
from flask import request, redirect, url_for, flash
from flask_login import current_user

def login_required(f):
   #"""Decorator para rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    #"""Decorator para rotas que requerem privilégios de admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Você precisa estar logado para acessar esta área.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
            
        if not current_user.is_admin:
            flash('Acesso permitido apenas para administradores.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, *kwargs)
    return decorated_function

def anonymous_required(f):
    #decorators para usuario nao logado
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if current_user.is_authenticaded:
            flash('Você ja está logado', 'info')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function
        