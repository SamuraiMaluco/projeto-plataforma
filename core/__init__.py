# /core/__init__.py
# A "fábrica" da aplicação. Constrói e configura a instância do Flask.
import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

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
    from modules.auth.routes import init_auth_routes
    from modules.admin.routes import init_admin_routes
    from modules.content.routes import init_content_routes
    from modules.exams.routes import init_exams_routes
    from modules.payments.routes import init_payments_routes
    from modules.progress.routes import init_progress_routes

    init_auth_routes(app)
    init_admin_routes(app)
    init_content_routes(app)
    init_exams_routes(app)
    init_payments_routes(app)
    init_progress_routes(app)

    return app