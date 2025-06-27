from .routes import bp as core_bp
from .extensions import db, login_manager

def init_core(app):
    """Inicializa o módulo core"""
    app.register_blueprint(core_bp)
    
    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configuração do login manager
    login_manager.login_view = 'auth.login'