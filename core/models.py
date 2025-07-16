from core.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique=True)
    senha = db.Column(db.String(255), nullable = False)
    assinatura_valida_ate = db.Column(db.DateTime, default=None)
    