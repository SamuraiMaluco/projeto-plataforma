from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from core.extensions import db
# 1. Importações Corretas (Module em vez de Content)
from .models import Subject, Module, Lesson, LessonProgress

bp = Blueprint('content', __name__, url_prefix='/content')

@bp.route('/')
@login_required
def index():
    """Lista todas as matérias disponíveis"""
    subjects = Subject.query.all()
    return render_template('content/index.html', subjects=subjects)

@bp.route('/materia/<string:slug>')
@login_required
def subject_detail(slug):
    """Mostra os módulos (capítulos) de uma matéria"""
    subject = Subject.query.filter_by(slug=slug).first_or_404()
    
    # 2. Busca Módulos ordenados
    modules = Module.query.filter_by(subject_id=subject.id).order_by(Module.order).all()
    
    return render_template('content/subject.html', subject=subject, modules=modules)

@bp.route('/aula/<int:lesson_id>')
@login_required
def lesson_player(lesson_id):
    """Player da aula (Vídeo, Áudio ou PDF)"""
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Verifica permissão (opcional)
    # if not lesson.is_free and not current_user.has_subscription():
    #     return redirect(url_for('payments.index'))

    # Marca como visto
    progress = LessonProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson.id).first()
    if not progress:
        progress = LessonProgress(user_id=current_user.id, lesson_id=lesson.id, completed=True)
        db.session.add(progress)
        db.session.commit()

    # 3. Lógica Próximo/Anterior usando module_id
    previous_lesson = Lesson.query.filter_by(module_id=lesson.module_id)\
        .filter(Lesson.order < lesson.order)\
        .order_by(Lesson.order.desc()).first()
        
    next_lesson = Lesson.query.filter_by(module_id=lesson.module_id)\
        .filter(Lesson.order > lesson.order)\
        .order_by(Lesson.order.asc()).first()

    return render_template('content/player.html', 
                         lesson=lesson, 
                         previous_lesson=previous_lesson, 
                         next_lesson=next_lesson)

# Esta função é CRUCIAL para o app funcionar
def init_content_routes(app):
    app.register_blueprint(bp)