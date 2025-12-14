import requests
import os
from dotenv import load_dotenv
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from core.extensions import db
from modules.auth.models import User
from datetime import datetime, timedelta

# Configuração
basedir = os.path.abspath(os.path.dirname(__file__))
root_dir = os.path.join(basedir, '..', '..')
load_dotenv(os.path.join(root_dir, '.env'))

# Mude para False quando for colocar o site no ar de verdade!
USAR_SANDBOX = True 
TOKEN = os.getenv('PAGBANK_TOKEN')

# URLs do PagBank
if USAR_SANDBOX:
    URL_CRIAR_CHECKOUT = "https://sandbox.api.pagseguro.com/checkouts"
else:
    URL_CRIAR_CHECKOUT = "https://api.pagseguro.com/checkouts"

bp = Blueprint('payments', __name__, url_prefix='/payments')

# Preços em Centavos (R$ 39,90 = 3990)
PRECOS = {
    'mensal': {'valor': 3990, 'nome': 'Plano Mensal'},
    'anual_avista': {'valor': 39990, 'nome': 'Plano Anual'},
    'anual_parcelado': {'valor': 47990, 'nome': 'Plano Anual Parcelado'}
}

@bp.route('/')
@login_required
def index():
    if current_user.assinatura_valida_ate and current_user.assinatura_valida_ate > datetime.utcnow():
        flash('Você já possui uma assinatura ativa!', 'info')
        return redirect(url_for('core.home'))
    return render_template('pagamento.html')

@bp.route('/checkout/<string:plano>')
@login_required
def checkout(plano):
    if not TOKEN:
        flash('Erro: Token do PagBank não configurado no .env', 'danger')
        return redirect(url_for('payments.index'))

    if plano not in PRECOS:
        flash('Plano inválido.', 'danger')
        return redirect(url_for('payments.index'))

    dados_plano = PRECOS[plano]
    
    # Payload para a API do PagBank
    payload = {
        "reference_id": f"user_{current_user.id}_{plano}",
        "customer": {
            "name": current_user.username,
            "email": current_user.email,
            "tax_id": "12345678909", # CPF de Teste (Sandbox aceita qualquer um válido)
        },
        "items": [
            {
                "reference_id": plano,
                "name": dados_plano['nome'],
                "quantity": 1,
                "unit_amount": dados_plano['valor']
            }
        ],
        "redirect_url": url_for('payments.aprovado', _external=True),
        # notification_urls é opcional no teste, mas bom ter
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    try:
        response = requests.post(URL_CRIAR_CHECKOUT, json=payload, headers=headers)
        
        if response.status_code == 201: # Sucesso (Created)
            dados = response.json()
            # Pega o link de pagamento na resposta
            for link in dados.get('links', []):
                if link['rel'] == 'PAY':
                    return redirect(link['href'])
            
            flash('Erro: Link de pagamento não encontrado.', 'warning')
        else:
            print(f"Erro PagBank: {response.text}")
            flash('Erro ao criar pagamento no PagBank.', 'danger')

    except Exception as e:
        print(f"Erro de conexão: {e}")
        flash('Erro interno ao processar pagamento.', 'danger')

    return redirect(url_for('payments.index'))

@bp.route('/aprovado')
@login_required
def aprovado():
    user = User.query.get(current_user.id)
    user.assinatura_valida_ate = datetime.utcnow() + timedelta(days=30)
    db.session.commit()
    flash("Pagamento Iniciado! Acesso liberado temporariamente.", "success")
    return redirect(url_for('core.home'))

# Função obrigatória para o Flask carregar o módulo
def init_payments_routes(app):
    app.register_blueprint(bp)