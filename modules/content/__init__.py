from .routes import bp as content_bp
from .models import load_initial_data
from core.extensions import db
def load_initial_data():
    # Carrega dados iniciais, se necessário
    pass

def init_content(app):
    #"""Inicializa o módulo de conteúdo#
    app.register_blueprint(content_bp, url_prefix='/content')
    
    # Carrega dados iniciais
    with app.app_context():
        db.create_all()
        