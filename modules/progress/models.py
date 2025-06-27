from core.extensions import db
from datetime import datetime

class LessonProgress(db.Model):
   # """Armazena o progresso do usuário em cada aula (Fase 2)"""
    __tablename__ = 'lesson_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    
    # Status básico (podemos adicionar mais campos depois)
    is_completed = db.Column(db.Boolean, default=False)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    
    # Relacionamentos (otimizados para consultas frequentes)
    user = db.relationship('User', backref='lessons_progress')
    lesson = db.relationship('Lesson', backref='user_progress_records')

    def __repr__(self):
        return f'<Progresso aula {self.lesson_id} - usuário {self.user_id}>'


class SubjectProgress(db.Model):
    #"""Progresso agregado por matéria (Fase 2 - opcional)"""
    __tablename__ = 'subject_progress'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
    
    # Métricas básicas
    completed_lessons = db.Column(db.Integer, default=0)
    total_lessons = db.Column(db.Integer, default=0)
    progress_percentage = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='subjects_progress')
    subject = db.relationship('Subject', backref='users_progress')


# Funções auxiliares para serem chamadas nas rotas
def update_lesson_progress(user_id, lesson_id, is_completed=False):
   # """Atualiza o progresso de uma aula específica"""
    progress = LessonProgress.query.filter_by(
        user_id=user_id,
        lesson_id=lesson_id
    ).first()

    if not progress:
        progress = LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id
        )
        db.session.add(progress)

    progress.is_completed = is_completed
    progress.last_accessed = datetime.utcnow()
    
    if is_completed and not progress.completion_date:
        progress.completion_date = datetime.utcnow()
    
    db.session.commit()
    return progress


def get_user_progress(user_id, subject_id=None):
   # """Obtém o progresso consolidado do usuário"""
    progress_data = {
        'total_completed': 0,
        'total_lessons': 0,
        'by_subject': {}
    }

    # Podemos implementar lógica mais sofisticada depois
    if subject_id:
        # Progresso específico por matéria
        pass
    else:
        # Progresso geral
        progress_data['total_completed'] = LessonProgress.query.filter_by(
            user_id=user_id,
            is_completed=True
        ).count()

    return progress_data


def init_progress_models():
    """Cria as tabelas de progresso"""
    db.create_all()