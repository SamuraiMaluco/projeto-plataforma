from core import create_app
from core.extensions import db
from modules.auth.models import User
# CORREÇÃO 1: Importamos Module em vez de Content
from modules.content.models import Subject, Module, Lesson
import click

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Subject=Subject, Module=Module, Lesson=Lesson)

# --- COMANDO PARA CRIAR ADMIN ---
@app.cli.command("create-admin")
@click.option("--username", required=True, help="O nome de utilizador do administrador.")
@click.option("--email", required=True, help="O e-mail do administrador.")
@click.option("--password", required=True, help="A senha do administrador.")
def create_admin(username, email, password):
    """Cria um novo utilizador administrador."""
    print("A criar o utilizador administrador...")
    try:
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

# --- COMANDO PARA POPULAR BANCO (CORRIGIDO) ---
@app.cli.command("seed-db")
def seed_db():
    """Popula a base de dados com a nova estrutura (Matéria -> Módulo -> Aula)"""
    print("A popular a base de dados com dados iniciais...")
    try:
        # 1. Criar a Matéria (Subject)
        # Note que adicionamos slug e icon que definimos no models.py
        matematica = Subject(
            name="Matemática Financeira", 
            slug="matematica-financeira", 
            icon="calculator",
            description="Aprenda a cuidar do seu dinheiro."
        )
        db.session.add(matematica)
        db.session.commit() # Comita para gerar o ID da matéria

        # 2. Criar um Módulo/Capítulo (Module)
        # CORREÇÃO: Usamos 'Module' e ligamos ele à matéria (subject_id)
        modulo_boas_vindas = Module(
            title="Módulo 1: Introdução", 
            order=1, 
            subject=matematica # Relacionamento
        )
        db.session.add(modulo_boas_vindas)
        db.session.commit() # Comita para gerar o ID do módulo

        # 3. Criar Aulas (Lessons)
        # CORREÇÃO: Corrigido 'tittle' para 'title' e ligamos ao Módulo (não à matéria)
        
        # Aula 1: Texto
        aula1 = Lesson(
            title="Bem-vindo ao Curso", 
            order=1,
            content_text="<p>Seja bem vindo ao curso de matemática.</p>",
            module=modulo_boas_vindas # Liga ao módulo criado acima
        )

        # Aula 2: Exemplo de Vídeo
        aula2 = Lesson(
            title="O que são Juros?", 
            order=2,
            video_url="https://www.youtube.com/watch?v=VIDEO_EXEMPLO",
            content_text="Explicação sobre juros simples.",
            module=modulo_boas_vindas
        )

        # Aula 3: Exemplo de PDF
        aula3 = Lesson(
            title="Apostila em PDF", 
            order=3,
            pdf_file="apostila_intro.pdf",
            module=modulo_boas_vindas
        )

        db.session.add_all([aula1, aula2, aula3])
        db.session.commit()
        
        print("Base de dados populada com sucesso! (Estrutura: Matéria -> Módulo -> Aulas)")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        db.session.rollback()

if __name__ == '__main__':
    app.run(debug=True)