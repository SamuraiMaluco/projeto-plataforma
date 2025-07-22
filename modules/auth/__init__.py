from .routes import bp as auth_bp
from .models import create_default_admin
from flask import Blueprint
import os
from werkzeug.security import generate_password_hash
from core.extensions import db
from modules.auth.models import User



bp = Blueprint('auth', __name__)

# Importe as rotas no final para evitar imports circulares
from . import routes
def create_default_admin():
    username = os.getenv('ADMIN_USERNAME')
    email = os.getenv('ADMIN_EMAIL')
    senha = os.getenv('ADMIN_PASSWORD')

    if not username or not email or not senha:
        print('⚠️ Dados do admin ausentes no .env. Admin não criado.')
        return
    if not User.query.filter_by(username=username).first():
        admin = User(
        Username=username,
        email=email,
        senha=generate_password_hash(senha),
        is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f'✅ Admin padrão "{username}" criado com sucesso!')
    else:
        print('ℹ️ Admin já existente, nada foi criado.')


def init_auth(app):
    #importa localmente dentro da função
    from .models import create_default_admin
    create_default_admin()