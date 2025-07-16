from core.extensions import db
from flask_login import UserMixin
from datetime import datetime
from core.extensions import db
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'auth_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Relacionamentos
    subscription = db.relationship('Subscription', back_populates='user', uselist=False)
    transactions = db.relationship('Transaction', back_populates='user')

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    plan_type = db.Column(db.String(20))  # premium, basic, trial
    valid_until = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(20))
    
    # Relacionamentos
    user = db.relationship('User', back_populates='subscription')
    payments = db.relationship('Payment', back_populates='subscription')
    def __repr__(self):
        return f'<User {self.username}>'
    
    
    #criando um admin
    def create_default_admin():
        from .models import User 
        
        #verificar se existe um cargo de admin
        admin_exists = User.query.filter_by(username='admin').first()
        if not admin_exists:
            admin = User(
                username = 'admin',
                email='admindb@user.com',
                password=generate_password_hash("senha123"),
                is_admin=True
            )
        db.session.ad(admin)
        db.session.commit()
        print('Administrador criado com sucesso!')
        