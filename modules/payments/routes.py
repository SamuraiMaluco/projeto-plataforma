# /modules/payments/routes.py
from flask import Blueprint
from flask_login import login_required

bp = Blueprint('payments', __name__, url_prefix='/payments')

@bp.route('/checkout')
@login_required
def checkout():
    return "Página de Checkout"

def init_payments_routes(app):
    app.register_blueprint(bp)