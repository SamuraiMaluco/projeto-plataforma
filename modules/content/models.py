from core.extensions import db
from datetime import datetime

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(30), default='book')
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    chapters = db.relationship('Chapter', back_populates='subject', order_by='Chapter.order')

class Chapter(db.Model):
    __tablename__ = 'chapters'
    
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True)
    order = db.Column(db.Integer)
    description = db.Column(db.Text)
    
    # Relacionamentos
    subject = db.relationship('Subject', back_populates='chapters')
    lessons = db.relationship('Lesson', back_populates='chapter', order_by='Lesson.order')

class Lesson(db.Model):
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)
    video_url = db.Column(db.String(255))
    duration = db.Column(db.Integer)  # in minutes
    is_free = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relacionamentos
    chapter = db.relationship('Chapter', back_populates='lessons')

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'url': self.url,
            'ordem': self.ordem,
            'pago': self.pago
        }