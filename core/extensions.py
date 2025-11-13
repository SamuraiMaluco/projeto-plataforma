# /core/extensions.py
# Centraliza a criação dos objetos de extensão para evitar importações circulares.
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para aceder a esta página.'
login_manager.login_message_category = 'info'


# --- INÍCIO DA CORREÇÃO ---
# Esta função é o "tradutor" que o Flask-Login precisa.
# Ele recebe o user_id (que estava guardado na sessão)
# e deve retornar o objeto User correspondente.
@login_manager.user_loader
def load_user(user_id):
    # Nós importamos o modelo User AQUI DENTRO da função
    # para evitar um erro de "importação circular",
    # já que o modules/auth/models.py precisa importar o 'db'
    # que está neste mesmo arquivo.
    from modules.auth.models import User
    
    # O user_id vem da sessão como string, então convertemos para int
    return User.query.get(int(user_id))
# --- FIM DA CORREÇÃO ---