from run import create_app
from core.extensions import db
from modules.auth.models import User

app = create_app()

def promote_to_admin():
    with app.app_context():
        print("--- PROMOVER USUÁRIO A ADMIN ---")
        email = input("Digite o email do usuário que será Admin: ")
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            user.is_admin = True
            db.session.commit()
            print(f"\n✅ SUCESSO! O usuário {user.name} ({user.email}) agora é um ADMINISTRADOR.")
            print("Reinicie o site e faça login novamente para ver as opções.")
        else:
            print(f"\n❌ Erro: Usuário com email '{email}' não encontrado.")

if __name__ == "__main__":
    promote_to_admin()