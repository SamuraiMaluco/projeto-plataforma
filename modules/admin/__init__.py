from .routes import bp as admin_bp
from .models import init_admin_models

def init_admin(app):
    """Inicializa o módulo admin"""
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Inicializa modelos específicos
    with app.app_context():
        init_admin_models()