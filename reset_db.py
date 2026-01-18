
from run import create_app
from core.extensions import db

app = create_app()

with app.app_context():
    print(" Apagando tabelas antigas...")
    db.drop_all()
    
    print(" Criando tabelas novas (com a coluna description)...")
    db.create_all()
    
    print(" Banco de dados atualizado com sucesso!")