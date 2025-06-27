from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import current_user
from datetime import datetime
from modules.auth.models import User

bp = Blueprint('core', __name__)

@bp.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if session.get('primeira_visita', True):
        session['primeira_visita'] = False
        mensagem = 'Seja muito bem-vindo'
    else:
        mensagem = 'Bem-vindo de volta'
        
    assinatura_ativa = current_user.assinatura_valida_ate and current_user.assinatura_valida_ate > datetime.now()
    
    return render_template('core/home.html',
                         email=current_user.email,
                         username=current_user.username,
                         mensagem=mensagem,
                         assinatura=assinatura_ativa)

@bp.route('/sobre')
def sobre():
    return render_template('core/sobre.html')