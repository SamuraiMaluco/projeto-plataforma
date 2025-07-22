from .routes import bp as admin_bp
from flask import Blueprint
#from .models import init_admin_models - a ideia era ter um banco de dados para o admin mas 


bp = Blueprint('admin', __name__, url_prefix='/admin')

from . import routes

@bp.route('/')
def painel_admin():
    return render_template('admin/dashboard.html')

def init_admin(app):
    """Inicializa o módulo admin"""
    app.register_blueprint(admin_bp,__name__, url_prefix='/admin')
    
    # Inicializa modelos específicos
   ##    init_admin_models()