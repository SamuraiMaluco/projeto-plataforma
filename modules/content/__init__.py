from .routes import bp as content_bp
from .models import load_initial_data

def init_content(app):
    """Inicializa o módulo de conteúdo"""
    app.register_blueprint(content_bp, url_prefix='/content')
    
    # Carrega dados iniciais
    with app.app_context():
        load_initial_data()