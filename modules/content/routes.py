# /modules/content/routes.py

# A importação correta vem diretamente do flask_login
from flask import Blueprint
from flask_login import login_required 

bp = Blueprint('content', __name__, url_prefix='/content')

@bp.route('/subjects')
@login_required # Agora o decorador pode ser usado sem erro
def list_subjects():
    return "Lista de Matérias (requer login)"

@bp.route('/subject/<int:subject_id>')
@login_required
def view_subject(subject_id):
    return f"Visualizando conteúdos da matéria {subject_id} (requer login)"

def init_content_routes(app):
    app.register_blueprint(bp)