# /core/__init__.py
import os
from flask import Flask, render_template
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ['true', '1']

    # Inicializa as extensões
    from .extensions import db, migrate, login_manager, csrf
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Regista todos os módulos (Blueprints)
    from core.routes import init_core_routes
    from modules.auth.routes import init_auth_routes
    from modules.admin.routes import init_admin_routes
    from modules.content.routes import init_content_routes
    from modules.exams.routes import init_exams_routes
    from modules.payments.routes import init_payments_routes
    
    # --- ### A CORREÇÃO ESTÁ AQUI ### ---
    # Esta linha estava faltando
    from modules.progress.routes import init_progress_routes
    # --- FIM DA CORREÇÃO ---

    init_core_routes(app)
    init_auth_routes(app)
    init_admin_routes(app)
    init_content_routes(app)
    init_exams_routes(app)
    init_payments_routes(app)
    init_progress_routes(app) # <-- Agora esta linha vai funcionar
  
    @app.template_filter('time_ago')
    def format_time_ago(value):
        """Formata um datetime para 'X tempo atrás'."""
        if not isinstance(value, datetime):
            return str(value) # Retorna o valor se não for uma data
        
        now = datetime.utcnow()
        diff = now - value
        
        seconds = diff.total_seconds()
        days = diff.days

        if days > 7:
            return value.strftime('%d/%m/%Y') # Ex: 10/11/2025
        elif days > 1:
            return f'{days} dias atrás'
        elif days == 1:
            return 'ontem'
        elif seconds > 7200: # Mais de 2 horas
            return f'{int(seconds // 3600)} horas atrás'
        elif seconds > 3600: # Mais de 1 hora
            return '1 hora atrás'
        elif seconds > 120: # Mais de 2 minutos
            return f'{int(seconds // 60)} minutos atrás'
        elif seconds > 60: # Mais de 1 minuto
            return '1 minuto atrás'
        else:
            return 'agora mesmo'

    @app.context_processor
    def inject_now():
        """
        Injeta a variável 'now' (com a data/hora atual) em todos os templates
        para ser usada no rodapé (copyright).
        """
        return {'now': datetime.utcnow()}
  
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error/500.html'), 500

    return app