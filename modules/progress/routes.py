# /modules/progress/routes.py
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from .services import ProgressService

bp = Blueprint('progress', __name__, url_prefix='/progress')

@bp.route('/complete-lesson/<int:lesson_id>', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    try:
        lesson_progress, subject_progress = ProgressService.complete_lesson(current_user.id, lesson_id)
        return jsonify({
            'status': 'success',
            'data': {
                'lesson': {'completed': lesson_progress.is_completed},
                'subject': {'progress': subject_progress.progress_percentage}
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

def init_progress_routes(app):
    app.register_blueprint(bp)