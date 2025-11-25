# populate_db.py
from core import create_app
from core.extensions import db
from modules.content.models import Subject, Content, Lesson
from modules.auth.models import User

app = create_app()

def popular_banco():
    with app.app_context():
        print("Recriando banco de dados...")
        db.drop_all()
        db.create_all()

        # --- 1. CRIAR USUÁRIO TESTE ---
        print(" Criando usuário admin...")
        admin = User(username='admin', email='admin@study.com', is_admin=True)
        admin.set_password('12345678') # Senha simples para teste
        db.session.add(admin)

        # --- 2. CRIAR MATÉRIAS ---
        print(" Criando matérias...")
        matematica = Subject(name='Matemática', slug='matematica', icon='calculator')
        portugues = Subject(name='Português', slug='portugues', icon='book')
        ingles = Subject(name='Inglês', slug='ingles', icon='globe')
        
        db.session.add_all([matematica, portugues, ingles])
        db.session.commit()

        # --- 3. CRIAR CONTEÚDOS E AULAS (MATEMÁTICA) ---
        print(" Criando aulas de Matemática...")
        
        # Módulo 1: Álgebra
        algebra = Content(title='Módulo 1: Álgebra Básica', subject=matematica, order=1)
        db.session.add(algebra)
        
        aula1 = Lesson(
            title='Introdução às Equações',
            order=1,
            content=algebra,
            type='video',
            is_free=True,
            duration=15,
            # Vídeo de exemplo (Big Buck Bunny é clássico para testes)
            media_url='http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
            thumbnail_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/800px-Big_buck_bunny_poster_big.jpg',
            content_text='<p>Nesta aula vamos aprender os conceitos básicos de equações de primeiro grau.</p>'
        )
        
        aula2 = Lesson(
            title='Fatoração Simples',
            order=2,
            content=algebra,
            type='video',
            is_free=False, # Premium
            duration=20,
            media_url='http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
            thumbnail_url='https://upload.wikimedia.org/wikipedia/commons/0/0c/Elephants_Dream_poster.jpg',
            content_text='<p>Aprofundando em fatoração e produtos notáveis.</p>'
        )

        # --- 4. CRIAR CONTEÚDOS E AULAS (PORTUGUÊS) ---
        print("📖 Criando aulas de Português...")
        
        gramatica = Content(title='Gramática Essencial', subject=portugues, order=1)
        db.session.add(gramatica)
        
        aula3 = Lesson(
            title='Uso dos Porquês',
            order=1,
            content=gramatica,
            type='video',
            is_free=True,
            duration=10,
            media_url='http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
            content_text='<p>Entenda definitivamente quando usar cada tipo de porquê.</p>'
        )

        db.session.add_all([aula1, aula2, aula3])
        db.session.commit()
        
        print("✅ Banco de dados populado com sucesso!")
        print("👉 Login Admin: admin@study.com / 12345678")

if __name__ == '__main__':
    popular_banco()