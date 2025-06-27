from .routes import bp as auth_bp
from .models import create_default_admin

def init_auth(app):
    """Inicializa o módulo de autenticação"""
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Cria usuário admin padrão se não existir
    with app.app_context():
        create_default_admin()