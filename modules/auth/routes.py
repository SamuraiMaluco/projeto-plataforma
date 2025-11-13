# /modules/auth/routes.py
# Rotas para login, logout e registo.

# Imports necessários do Flask e Flask-Login
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

# Imports do nosso projeto
from .models import User
from .services import AuthService
from core.extensions import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se o utilizador já estiver logado, redireciona para a home
    if current_user.is_authenticated:
        return redirect(url_for('core.home')) 

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Procura o utilizador na base de dados pelo email
        user = User.query.filter_by(email=email).first()

        # Verifica se o utilizador existe E se a senha está correta
        if user and user.check_password(password):
            # Se sim, faz o login
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            # Redireciona para a página principal (home)
            return redirect(url_for('core.home'))
        else:
            # Se não, mostra uma mensagem de erro
            flash('Credenciais inválidas. Tente novamente.', 'danger')

    # Se for um pedido GET, apenas mostra a página de login
    return render_template('auth/login.html')


# --- ESTA É A FUNÇÃO QUE ESTAVA FALTANDO ---
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Se o utilizador já estiver logado, redireciona para a home
    if current_user.is_authenticated:
        return redirect(url_for('core.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # Usamos o nosso AuthService
            novo_user = AuthService.criar_usuario(
                username=username,
                email=email,
                senha=password
            )
            
            # Se o utilizador foi criado com sucesso, faz o login dele imediatamente
            login_user(novo_user)
            flash('Conta criada com sucesso! Bem-vindo.', 'success')
            return redirect(url_for('core.home'))

        except ValueError as e:
            # Se o AuthService levantar um erro (ex: user já existe, senha fraca),
            # mostramos esse erro ao utilizador.
            flash(str(e), 'danger')
        except Exception as e:
            # Captura outros erros inesperados (ex: falha de BD)
            db.session.rollback() # Desfaz qualquer alteração pendente na BD
            flash(f'Ocorreu um erro inesperado: {e}', 'danger')

    # Se for um pedido GET, apenas mostra a página de registo
    return render_template('auth/register.html')


@bp.route('/logout')
@login_required # Garante que só utilizadores logados podem fazer logout
def logout():
    logout_user()
    flash('Sessão terminada com sucesso.', 'info')
    return redirect(url_for('auth.login'))


def init_auth_routes(app):
    app.register_blueprint(bp)