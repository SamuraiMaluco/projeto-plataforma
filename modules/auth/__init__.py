from .routes import bp as auth_bp
from .models import create_default_admin
from flask import Blueprint

bp = Blueprint('auth', __name__)

# Importe as rotas no final para evitar imports circulares
from . import routes



def init_auth(app):
    #importa localmente dentro da função
    from .models import create_default_admin
    create_default_admin()