from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import datetime
from core.extensions import db
from core.decorators import admin_required
from .models import Subject, Module, Lesson, LessonProgress

bp = Blueprint('content', __name__, url_prefix='/content')

# =========================================================
# ROTAS DE VISUALIZAÇÃO (ALUNO)
# =========================================================

@bp.route('/')
@login_required 
def index():
    """Lista todas as matérias disponíveis."""
    subjects = Subject.query.all()
    return render_template('content/index.html', subjects=subjects)

@bp.route('/materia/<string:slug>')
@login_required
def subject_detail(slug):
    """Mostra detalhes da matéria e seus módulos."""
    subject = Subject.query.filter_by(slug=slug).first_or_404()
    modules = Module.query.filter_by(subject_id=subject.id).order_by(Module.order).all()
    return render_template('content/subject.html', subject=subject, modules=modules)

@bp.route('/aula/<int:lesson_id>')
@login_required
def lesson_detail(lesson_id):
    """Player da aula."""
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
    
    # Navegação (Anterior / Próxima)
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

# =========================================================
# ROTAS DE GERENCIAMENTO (ADMIN)
# =========================================================

@bp.route('/add-subject', methods=['GET', 'POST'])
@login_required
@admin_required
def add_subject():
    """Cria uma nova matéria."""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        icon = request.form.get('icon', 'book')
        
        # Cria slug automático
        slug = name.lower().replace(' ', '-')
        
        new_subject = Subject(name=name, description=description, icon=icon, slug=slug)
        db.session.add(new_subject)
        db.session.commit()
        flash('Matéria criada com sucesso!', 'success')
        return redirect(url_for('content.index'))
    
    return render_template('content/add_edit.html', type='subject')

@bp.route('/add-module/<int:subject_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_module(subject_id):
    """Adiciona um módulo a uma matéria."""
    subject = Subject.query.get_or_404(subject_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        new_module = Module(title=title, description=description, subject_id=subject.id)
        db.session.add(new_module)
        db.session.commit()
        flash(f'Módulo adicionado em {subject.name}!', 'success')
        return redirect(url_for('content.subject_detail', slug=subject.slug))
        
    return render_template('content/add_edit.html', type='module', parent=subject)

@bp.route('/add-lesson/<int:module_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_lesson(module_id):
    """Adiciona uma aula a um módulo."""
    module = Module.query.get_or_404(module_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        video_url = request.form.get('video_url')
        content_text = request.form.get('content_text')
        duration = request.form.get('duration')
        is_free = request.form.get('is_free') == 'on'
        
        new_lesson = Lesson(
            title=title, 
            video_url=video_url, 
            content_text=content_text,
            duration=int(duration) if duration else 0,
            is_free=is_free,
            module_id=module.id
        )
        db.session.add(new_lesson)
        db.session.commit()
        flash('Aula adicionada com sucesso!', 'success')
        return redirect(url_for('content.subject_detail', slug=module.subject.slug))

    return render_template('content/add_edit.html', type='lesson', parent=module)

@bp.route('/delete-lesson/<int:lesson_id>', methods=['POST'])
@login_required
@admin_required
def delete_lesson(lesson_id):
    """Deleta uma aula."""
    lesson = Lesson.query.get_or_404(lesson_id)
    # Remove progressos antes de deletar
    LessonProgress.query.filter_by(lesson_id=lesson.id).delete()
    
    db.session.delete(lesson)
    db.session.commit()
    flash('Aula removida com sucesso.', 'success')
    return redirect(url_for('content.index'))

def init_content_routes(app):
    app.register_blueprint(bp)