from flask import Blueprint, request, flash, redirect, url_for, session, render_template
from core.models import User
from core.extensions import db
from core.decorators import login_required
from core.utils import validar_senha
from werkzeug.security import generate_password_hash, check_password_hash
from . .auth.models import User
bp = Blueprint('auth', __name__, url_prefix='/auth')
from .routes import bp as auth_bp

def init_auth(app):
    app.register_blueprint(auth_bp)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha, senha):
            session['email'] = email
            return redirect(url_for('main.home'))
        
        flash('Credenciais inválidas', 'danger')
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Implementação similar, usando serviços
    if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            senha = request.form.get('senha')

    if not username or not email or not senha:
            flash('Por favor, preencha todos os campos', 'error')
            return render_template('auth/register.html')

    if not validar_senha(senha):
            flash('A senha deve conter pelo menos 8 caracteres, um número, uma letra maiúscula e um caracter especial', 'error')
            return redirect(url_for('auth.register'))

    if User.query.filter_by(username=username).first():
            flash('Este nome já existe!', 'error')
            return redirect(url_for('auth.register'))
        
    if User.query.filter_by(email=email).first():
            flash('Este email já foi cadastrado!', 'error')
            return redirect(url_for('auth.register'))

    new_user = User(
            username=username,
            email=email,
            senha=generate_password_hash(senha)
        )
        
    db.session.add(new_user)
    db.session.commit()
    flash('Cadastro concluído!', 'success')
    return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('auth.login'))