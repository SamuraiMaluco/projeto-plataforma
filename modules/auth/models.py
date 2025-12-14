

# A linha mais importante é esta, que importa o objeto db
from core.extensions import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)

    # Relações com outros módulos
    exam_attempts = db.relationship('ExamAttempt', back_populates='user', lazy='dynamic')
    payments = db.relationship('Payment', back_populates='user', lazy='dynamic')
    lesson_progress = db.relationship('LessonProgress', back_populates='user', lazy='dynamic')
    subject_progress = db.relationship('SubjectProgress', back_populates='user', lazy='dynamic')
    assinatura_valida_ate = db.Column(db.DateTime, nullable=True)
    
    #outros modulos relacionados
    exam_attempts = db.relationship('ExamAttempt', back_populates='user', lazy='dynamic')
    
    
    @property
    def is_premium(self):
        #propriedade inteligente: retorna True se a data for futura
        if self.assinatura_valida_ate:
            return self.assinatura_valida_ate > datetime.utcnow()
        return False
    
    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)