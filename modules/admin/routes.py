from flask import Blueprint, render_template
from . import bp #blueprint do __init__.py
@bp.route('/dashboard')
def dashboard():
    return "Painel Administrativo"

bp = Blueprint('admin', __name__, url_prefix='/admin')
