
from core.extensions import db
from core.utils import validar_senha

#importando o user para consultar e criar
from .models import User

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
            
        )
        
        #metodo set_password do modelo User
        novo_user.set_password(senha)
        
        db.session.add(novo_user)
        db.session.commit()
        return novo_user