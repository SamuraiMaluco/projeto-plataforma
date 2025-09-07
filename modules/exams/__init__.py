from .models import init_exams_models
from .routes import bp as exams_bp

def init_exams(app):
    #"""Inicializa o módulo de simulados"""
    app.register_blueprint(exams_bp, url_prefix='/exams')
    
    # Inicializa modelos específicos
    with app.app_context():
        init_exams_models()