# /run.py
from core import create_app
# Adicione estas importações no topo
from core.extensions import db
from modules.auth.models import User
import click

app = create_app()

# ADICIONE ESTE BLOCO DE CÓDIGO NO FINAL DO FICHEIRO
@app.cli.command("create-admin")
@click.option("--username", required=True, help="O nome de utilizador do administrador.")
@click.option("--email", required=True, help="O e-mail do administrador.")
@click.option("--password", required=True, help="A senha do administrador.")
def create_admin(username, email, password):
    """Cria um novo utilizador administrador."""
    print("A criar o utilizador administrador...")
    try:
        # Verifica se o utilizador ou e-mail já existem
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            print(f"Erro: O utilizador '{username}' ou o e-mail '{email}' já existe.")
            return

        admin = User(username=username, email=email, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Utilizador administrador '{username}' criado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        db.session.rollback()


if __name__ == '__main__':
    app.run(debug=True)