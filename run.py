# /run.py
from core import create_app
from core.extensions import db
from modules.auth.models import User
from modules.content.models import Subject, Content, Lesson
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

@app.cli.command("seed-db")
def seed_db():
    # Popula a base de dados com dados iniciais para testes
    print("A popular a base de dados com dados iniciais...")
    try:
        #cria uma Matéria (subject) de exemplo
        subject1 = Subject(name= "Introdução")

        #cria um conteúdo (Content) de exemplo
        content1 = Content(tittle = "bem-vindo", description = "Bem-vindo e obrigado por experimentatr nosso sistema")

        #cria uma lição (Lesson) de exemplo
        lesson1 = Lesson(tittle = "Primeira Lição", order=1, content = "Conteúdo da primeira lição", subject = subject1)
        lesson2 = Lesson(tittle = "Segunda Lição", order=2, content = "Conteúdo da segunda lição", subject = subject1)
        lesson3 = Lesson(tittle = "Terceira Lição", order=3, content = "Conteúdo da terceira lição", subject = subject1)

        db.session.add(subject1)
        db.session.add(content1)
        db.session.add(lesson1)
        db.session.add(lesson2)
        db.session.add(lesson3)
        
        db.session.commit()
        print("Base de dados populada com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        db.session.rollback()

if __name__ == '__main__':
    app.run(debug=True)