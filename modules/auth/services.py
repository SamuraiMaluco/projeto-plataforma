from core.models import User
from core.extensions import db
from core.utils import validar_senha

class AuthService:
    @staticmethod
    def criar_usuario(username, email, senha):
        if not validar_senha(senha):
            raise ValueError('Senha não atende aos requisitos')
            
        if User.query.filter((User.email == email) | (User.username == username)).first():
            raise ValueError('Usuário já existe')
            
        novo_user = User(
            username=username,
            email=email,
            senha=generate_password_hash(senha)
        )
        db.session.add(novo_user)
        db.session.commit()
        return novo_user