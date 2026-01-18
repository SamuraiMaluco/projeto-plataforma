from flask import Blueprint, render_template
from flask_login import login_required
from core.decorators import admin_required
from modules.content.models import Subject, Lesson

# Define o Blueprint como 'admin'
bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@login_required
@admin_required
def dashboard():
    """Painel principal com estatísticas do sistema"""
    total_subjects = Subject.query.count()
    total_lessons = Lesson.query.count()
    
    # Renderiza o template do dashboard
    return render_template('admin/dashboard.html', 
                         total_subjects=total_subjects, 
                         total_lessons=total_lessons)

def init_admin_routes(app):
    app.register_blueprint(bp)