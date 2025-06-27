from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from .services import ProgressService

bp = Blueprint('progress', __name__)

@bp.route('/track-lesson/<int:lesson_id>', methods=['POST'])
@login_required
def track_lesson(lesson_id):
    """Registra acesso a uma aula"""
    progress = ProgressService.record_lesson_access(current_user.id, lesson_id)
    return jsonify({
        'status': 'success',
        'data': {
            'lesson_id': lesson_id,
            'last_accessed': progress.last_accessed.isoformat()
        }
    })

@bp.route('/complete-lesson/<int:lesson_id>', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    """Marca aula como concluída"""
    lesson_progress, subject_progress = ProgressService.complete_lesson(
        current_user.id, 
        lesson_id
    )
    return jsonify({
        'status': 'success',
        'data': {
            'lesson': {
                'completed': lesson_progress.is_completed,
                'completion_date': lesson_progress.completion_date.isoformat()
            },
            'subject': {
                'subject_id': subject_progress.subject_id,
                'progress': subject_progress.progress_percentage
            }
        }
    })

@bp.route('/user-progress')
@login_required
def get_progress():
    """Obtém progresso consolidado"""
    subject_id = request.args.get('subject_id')
    progress = ProgressService.get_user_progress(
        current_user.id,
        subject_id=int(subject_id) if subject_id else None
    )
    return jsonify(progress)