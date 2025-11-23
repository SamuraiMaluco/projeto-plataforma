# /modules/content/routes.py

from flask import Blueprint, render_template # <<< Adicionado render_template
from flask_login import login_required 
from .models import Subject, Content, Lesson # <<< Modelos importados

bp = Blueprint('content', __name__, url_prefix='/content')

@bp.route('/subjects')
@login_required 
def list_subjects():
    # --- LÓGICA CORRIGIDA ---
    # Substituímos o texto "Lista de Matérias..." por código real.
    # Agora, ele busca os dados no banco e renderiza o seu template de aulas.
    
    # O seu template list_lesssons.html parece ser a melhor
    # página para listar as aulas, e ele espera 'lessons' e 'subjects'.
    lessons = Lesson.query.order_by(Lesson.order).all()
    subjects = Subject.query.all()

    return render_template('list_lesssons.html', 
                           lessons=lessons, 
                           subjects=subjects)
    # --- FIM DA CORREÇÃO ---

@bp.route('/subject/<int:subject_id>')
@login_required
def view_subject(subject_id):
    # (Esta rota ainda é um placeholder, mas a principal 'list_subjects' agora funciona)
    return f"Visualizando conteúdos da matéria {subject_id} (requer login)"

def init_content_routes(app):
    app.register_blueprint(bp)