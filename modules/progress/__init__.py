from .models import TrabalhoProgresso, MateriaProgresso
from .routes import bp as progress_bp
from core.extensions import db

def init_progress(app):
    #"""Inicializa o módulo de progresso"""
    app.register_blueprint(progress_bp, url_prefix='/progress')
    
    with app.app_context():
        db.create_all()