# /modules/content/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import datetime
from .models import Subject, Content, Lesson
from modules.progress.models import LessonProgress

bp = Blueprint('content', __name__, url_prefix='/content')

@bp.route('/subjects')
@login_required 
def list_subjects():
    # Busca todas as aulas ordenadas
    lessons = Lesson.query.order_by(Lesson.order).all()
    subjects = Subject.query.all()
    return render_template('list_lesssons.html', lessons=lessons, subjects=subjects)

@bp.route('/aula/<int:lesson_id>')
@login_required
def lesson_detail(lesson_id):
    # 1. Busca a aula no banco
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # 2. Verifica Permissão (Premium)
    # Se a aula não for grátis E o usuário não tiver assinatura válida...
    assinatura_ativa = current_user.assinatura_valida_ate and current_user.assinatura_valida_ate > datetime.utcnow()
    
    if not lesson.is_free and not assinatura_ativa:
        flash('Esta aula é exclusiva para assinantes. Assine para continuar!', 'warning')
        return redirect(url_for('payments.index'))

    # 3. Verifica se já foi completada pelo usuário
    progress = LessonProgress.query.filter_by(
        user_id=current_user.id, 
        lesson_id=lesson.id
    ).first()
    lesson.completed = progress.is_completed if progress else False

    # 4. Navegação (Anterior / Próxima)
    # Busca aulas do mesmo conteúdo (módulo) ordenadas
    all_lessons = Lesson.query.filter_by(content_id=lesson.content_id).order_by(Lesson.order).all()
    
    prev_lesson = None
    next_lesson = None
    
    for i, l in enumerate(all_lessons):
        if l.id == lesson.id:
            if i > 0:
                prev_lesson = all_lessons[i - 1]
            if i < len(all_lessons) - 1:
                next_lesson = all_lessons[i + 1]
            break

    return render_template('list_details.html', 
                           lesson=lesson,
                           prev_lesson=prev_lesson,
                           next_lesson=next_lesson)

@bp.route('/subject/<int:subject_id>')
@login_required
def view_subject(subject_id):
    return f"Visualizando conteúdos da matéria {subject_id} (requer login)"

def init_content_routes(app):
    app.register_blueprint(bp)