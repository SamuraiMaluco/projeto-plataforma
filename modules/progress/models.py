# /modules/progress/models.py
# Modelos para guardar o progresso do utilizador em lições e matérias.
from core.extensions import db
from datetime import datetime

class LessonProgress(db.Model):
    __tablename__ = 'lesson_progress'
    id = db.Column(db.Integer, primary_key=True)
    is_completed = db.Column(db.Boolean, default=False)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    user = db.relationship('User', back_populates='lesson_progress')
    lesson = db.relationship('Lesson', back_populates='user_progress')

class SubjectProgress(db.Model):
    __tablename__ = 'subject_progress'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
    completed_lessons = db.Column(db.Integer, default=0)
    total_lessons = db.Column(db.Integer, default=0)
    progress_percentage = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', back_populates='subject_progress')
    subject = db.relationship('Subject', back_populates='user_progress')