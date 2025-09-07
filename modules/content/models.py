# /modules/content/models.py

# Este ficheiro também precisa de importar o db
from core.extensions import db

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contents = db.relationship('Content', back_populates='subject', lazy='dynamic')
    user_progress = db.relationship('SubjectProgress', back_populates='subject', lazy='dynamic')

class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    subject = db.relationship('Subject', back_populates='contents')
    lessons = db.relationship('Lesson', back_populates='content', lazy='dynamic')

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    is_free = db.Column(db.Boolean, default=True)
    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'), nullable=False)
    content = db.relationship('Content', back_populates='lessons')
    user_progress = db.relationship('LessonProgress', back_populates='lesson', lazy='dynamic')