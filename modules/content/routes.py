from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import datetime
from core.extensions import db
from core.decorators import admin_required
from .models import Subject, Module, Lesson, LessonProgress

bp = Blueprint('content', __name__, url_prefix='/content')

# --- ROTA PRINCIPAL (DASHBOARD DO ALUNO) ---
# Renomeada para 'index' para bater com o menu lateral (content.index)
@bp.route('/')
@login_required 
def index():
    """Lista todas as matérias disponíveis."""
    subjects = Subject.query.all()
    # Certifique-se que o arquivo templates/content/index.html existe
    return render_template('content/index.html', subjects=subjects)

# --- DETALHES DA MATÉRIA ---
@bp.route('/materia/<string:slug>')
@login_required
def subject_detail(slug):
    subject = Subject.query.filter_by(slug=slug).first_or_404()
    modules = Module.query.filter_by(subject_id=subject.id).order_by(Module.order).all()
    return render_template('content/subject.html', subject=subject, modules=modules)

# --- PLAYER DA AULA ---
@bp.route('/aula/<int:lesson_id>')
@login_required
def lesson_detail(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Verifica assinatura
    assinatura_ativa = current_user.assinatura_valida_ate and current_user.assinatura_valida_ate > datetime.utcnow()
    if not lesson.is_free and not assinatura_ativa:
        flash('Esta aula é exclusiva para assinantes.', 'warning')
        return redirect(url_for('payments.index'))

    # Verifica progresso
    progress = LessonProgress.query.filter_by(
        user_id=current_user.id, 
        lesson_id=lesson.id
    ).first()
    
    # Navegação entre aulas
    all_lessons = Lesson.query.filter_by(module_id=lesson.module_id).order_by(Lesson.order).all()
    prev_lesson = None
    next_lesson = None
    
    for i, l in enumerate(all_lessons):
        if l.id == lesson.id:
            if i > 0: prev_lesson = all_lessons[i - 1]
            if i < len(all_lessons) - 1: next_lesson = all_lessons[i + 1]
            break

    return render_template('content/player.html', 
                           lesson=lesson,
                           previous_lesson=prev_lesson,
                           next_lesson=next_lesson)

# --- ROTA DE DELETAR (ADMIN) ---
@bp.route('/delete-lesson/<int:lesson_id>', methods=['POST'])
@login_required
@admin_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    LessonProgress.query.filter_by(lesson_id=lesson.id).delete()
    db.session.delete(lesson)
    db.session.commit()
    flash('Aula removida com sucesso.', 'success')
    return redirect(url_for('content.index'))

def init_content_routes(app):
    app.register_blueprint(bp)