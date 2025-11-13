# /core/routes.py
from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import current_user
from datetime import datetime # <<< Corrigido para utcnow
from modules.auth.models import User

bp = Blueprint('core', __name__)

# --- ROTA DUPLICADA REMOVIDA ---
# A rota @bp.route('/login') foi removida.
# A rota correta 'auth.login' já existe em modules/auth/routes.py

@bp.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if session.get('primeira_visita', True):
        session['primeira_visita'] = False
        mensagem = 'Seja muito bem-vindo'
    else:
        mensagem = 'Bem-vindo de volta'
        
    # Usando utcnow() para ser consistente com o webhook do MP
    assinatura_ativa = current_user.assinatura_valida_ate and current_user.assinatura_valida_ate > datetime.utcnow()
    
    # --- CORREÇÃO DE CAMINHO DO TEMPLATE ---
    # Corrigido de 'core/home.html' para 'home.html'
    return render_template('home.html',
                         email=current_user.email,
                         username=current_user.username,
                         mensagem=mensagem,
                         assinatura=assinatura_ativa)

@bp.route('/sobre')
def sobre():
    return render_template('core/sobre.html') # (Este template não foi enviado, mas mantive a rota)

# --- FUNÇÃO ADICIONADA ---
# Adicionamos a função init para seguir o padrão do projeto
def init_core_routes(app):
    app.register_blueprint(bp)