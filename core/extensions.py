from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# Inicialização das extensões
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def init_extensions(app):
    """Inicializa todas as extensões com o app Flask"""
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Configurações do Login Manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Configuração para nome de arquivos seguros
    app.extensions['secure_filename'] = secure_filename
    app.extensions['generate_password_hash'] = generate_password_hash
    app.extensions['check_password_hash'] = check_password_hash