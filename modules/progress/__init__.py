from .models import init_progress_models
from .routes import bp as progress_bp

def init_progress(app):
    """Inicializa o módulo de progresso"""
    app.register_blueprint(progress_bp, url_prefix='/progress')
    
    with app.app_context():
        init_progress_models()