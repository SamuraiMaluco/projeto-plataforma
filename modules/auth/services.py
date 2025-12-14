
# /modules/auth/services.py

from core.extensions import db
from core.utils import validar_senha
# --- IMPORTS QUE FALTAVAM ---
from .models import User 
# (Não precisamos importar generate_password_hash aqui se usarmos o set_password do modelo)

class AuthService:
    @staticmethod
    def criar_usuario(username, email, senha):
        # 1. Valida a senha
        if not validar_senha(senha):
            raise ValueError('A senha deve ter min. 8 caracteres, números e símbolos.')
            
        # 2. Verifica se usuário já existe
        if User.query.filter((User.email == email) | (User.username == username)).first():
            raise ValueError('Usuário ou email já existe.')
            
        # 3. Cria a instância do Usuário
        novo_user = User(
            username=username,
            email=email
        )
        
        # 4. Define a senha de forma segura (usando o método do seu modelo)
        # O seu modelo User já faz o 'generate_password_hash' aqui dentro
        novo_user.set_password(senha)
        
        # 5. Salva no banco
        db.session.add(novo_user)
        db.session.commit()
        
        return novo_user