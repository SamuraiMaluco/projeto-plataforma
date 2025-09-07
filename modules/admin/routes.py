# /modules/admin/routes.py
from flask import Blueprint
from core.decorators import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@admin_required
def dashboard():
    return "Bem-vindo ao Painel de Administração!"

def init_admin_routes(app):
    app.register_blueprint(bp)