from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from .services import ProgressService
# CORREÇÃO 1: Importamos do módulo content, onde os modelos vivem agora
from modules.content.models import LessonProgress, SubjectProgress

bp = Blueprint('progress', __name__, url_prefix='/progress')

@bp.route('/complete-lesson/<int:lesson_id>', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    try:
        # CORREÇÃO 2: Usamos o nome da função que está no seu services.py
        ProgressService.mark_lesson_completed(current_user.id, lesson_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

def init_progress_routes(app):
    app.register_blueprint(bp)