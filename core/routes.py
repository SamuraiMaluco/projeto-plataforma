
# /core/routes.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask_login import current_user
from datetime import datetime, timedelta # Importa datetime E timedelta
from modules.auth.models import User
from modules.progress.services import ProgressService # Importa o ProgressService

bp = Blueprint('core', __name__)

# A rota /login duplicada foi removida daqui. Ela está em modules/auth/routes.py.

@bp.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if session.get('primeira_visita', True):
        session['primeira_visita'] = False
        mensagem = 'Seja muito bem-vindo'
    else:
        mensagem = 'Bem-vindo de volta'
        
    # Usando utcnow() para ser consistente com o webhook
    assinatura_ativa = current_user.assinatura_valida_ate and current_user.assinatura_valida_ate > datetime.utcnow()
    
    # --- LÓGICA DE DADOS PARA O DASHBOARD ---
    
    # 1. Busca o progresso real do usuário
    progress_data = ProgressService.get_user_progress_summary(current_user.id)
    
    # 2. Cria dados FALSOS (dummy) para 'recent_activities'
    #    (Já que não temos essa lógica, mas o template home.html precisa)
    recent_activities_dummy = [
        {
            'icon': 'play-circle', 
            'title': 'Você começou a aula "Introdução"', 
            'timestamp': datetime.utcnow() - timedelta(minutes=10), 
            'status': 'success', 
            'status_label': 'Iniciado'
        },
        {
            'icon': 'check-circle', 
            'title': 'Você completou "Estruturas de Dados"', 
            'timestamp': datetime.utcnow() - timedelta(hours=2), 
            'status': 'primary', 
            'status_label': 'Concluído'
        }
    ]
    # --- FIM DA LÓGICA DE DADOS ---
    
    # Corrigido de 'core/home.html' para 'home.html'
    return render_template('home.html',
                         email=current_user.email,
                         username=current_user.username,
                         mensagem=mensagem,
                         assinatura=assinatura_ativa,
                         progress=progress_data, # Envia o progresso
                         recent_activities=recent_activities_dummy) # Envia as atividades

@bp.route('/sobre')
def sobre():
    # Esta é a função que eu apaguei sem querer
    return render_template('core/sobre.html') # (Assumindo que este template exista ou será criado)

def init_core_routes(app):
    # Esta é a outra função que eu apaguei
    app.register_blueprint(bp)