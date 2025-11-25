# /modules/content/models.py
from core.extensions import db

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True) # Para URLs bonitas (ex: /matematica)
    icon = db.Column(db.String(50)) # Ícone do FontAwesome (ex: 'calculator')
    
    contents = db.relationship('Content', back_populates='subject', lazy='dynamic')
    user_progress = db.relationship('SubjectProgress', back_populates='subject', lazy='dynamic')

class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    order = db.Column(db.Integer, default=0)
    
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    subject = db.relationship('Subject', back_populates='contents')
    lessons = db.relationship('Lesson', back_populates='content', lazy='dynamic')

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    is_free = db.Column(db.Boolean, default=True)
    
    # --- NOVOS CAMPOS PARA O PLAYER ---
    type = db.Column(db.String(20), default='video') # 'video', 'audio', 'pdf'
    media_url = db.Column(db.String(500)) # URL do vídeo/arquivo
    thumbnail_url = db.Column(db.String(500)) # Capa do vídeo
    content_text = db.Column(db.Text) # Descrição ou texto da aula
    duration = db.Column(db.Integer) # Duração em minutos
    # ----------------------------------

    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'), nullable=False)
    content = db.relationship('Content', back_populates='lessons')
    user_progress = db.relationship('LessonProgress', back_populates='lesson', lazy='dynamic')