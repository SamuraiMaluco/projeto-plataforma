from flask import Flask
from werkzeug.security import generate_password_hash  # Adicionado este import
from core.extensions import db, login_manager
from core import init_core
from modules.auth import init_auth
from modules.admin import init_admin
from modules.content import init_content
from modules.payments import init_payments
from modules.exams import init_exams  # Verifique se este módulo existe
from modules.progress import init_progress  # Nome corrigido (com dois 's')
import os

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_key') 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://th:Samurai3@localhost:5432/study_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CRON_API_KEY'] = 'sua_chave_secreta_aqui'
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {
        'video': ['mp4', 'mov', 'avi'],
        'audio': ['mp3', 'wav', 'ogg'],
        'image': ['jpg', 'jpeg', 'png', 'gif'],
        'document': ['pdf', 'docx', 'txt']
    }

    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Registrar módulos
    init_core(app)
    init_auth(app)
    init_admin(app)
    init_content(app)
    init_payments(app)
    init_exams(app)  # Se não usar simulados, remova esta linha
    init_progress(app)  # Nome corrigido

    # Criar admin padrão
    with app.app_context():
        db.create_all()
        from modules.auth.models import User
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@dev.com',
                senha=generate_password_hash('@admin123'),  # Agora reconhecido
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)