# /modules/auth/routes.py
# Rotas para login, logout e registo.
from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login')
def login():
    return "Página de Login"

@bp.route('/register')
def register():
    return "Página de Registo"

@bp.route('/logout')
def logout():
    return "Logout"

def init_auth_routes(app):
    app.register_blueprint(bp)