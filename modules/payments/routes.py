import requests
import os
from dotenv import load_dotenv
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from core.extensions import db
from modules.auth.models import User
from datetime import datetime, timedelta
import json
# Configuração
basedir = os.path.abspath(os.path.dirname(__file__))
root_dir = os.path.join(basedir, '..', '..')
load_dotenv(os.path.join(root_dir, '.env'))

# Mude para False quando for colocar o site no ar de verdade!
USAR_SANDBOX = True 
TOKEN = os.getenv('cdaf8bc7-a964-4ac2-8f40-9e3642081788330cab96498e8e09afec04672fb1561cff78-0436-41a9-bb5b-722369b4aa09')

# URLs do PagBank
if USAR_SANDBOX:
    URL_CRIAR_CHECKOUT = "https://sandbox.api.pagseguro.com/checkouts"
else:
    URL_CRIAR_CHECKOUT = "https://api.pagseguro.com/checkouts"

bp = Blueprint('payments', __name__, url_prefix='/payments')

@bp.route('/')
@login_required
def index():
    if current_user.assinatura_valida_ate and current_user.assinatura_valida_ate > datetime.utcnow():
        flash('Você já possui uma assinatura ativa!', 'info')
        return redirect(url_for('core.home'))
    return render_template('pagamento.html')

#rota para criar preferencia de pagamento

@bp.route('/criar-preferencia/<string:plano>')
@login_required
def criar_preferencia(plano):
# Preços em Centavos (R$ 39,90 = 3990)
#definindo os planos do token
    if plano == 'mensal':
        valor_centavos = 3990
        titulo_plano = "Assinatura Mensal"
        dias_acesso = 30

    elif plano == 'anual':
        valor_centavos = 39900
        titulo_plano = "Assinatura Anual"
        dias_acesso = 365

    elif plano == 'anual_parcelado':
        valor_centavos = 39900
        titulo_plano = "Assinatura Anual Parcelada"
        dias_acesso = 365

    else:
        flash('Plano inválido.', 'danger')
        return redirect(url_for('payments.index'))
    

    # salva na sessao o tempo de acesso para usar na volta (rota/aprovado)
    session['dias_acesso_pendente'] = dias_acesso

    #configura o API do pagbank
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "x-api-version": "4.0",
    }
    #dados do pedido
    payload = {
        "reference_id":f"REF_{current_user.id}_{int(dastetime.utcnow().timestamp())}",
        "customer": {
            "name": current_user.username,
            "email": current_user.email,
            "tax_id": "12345678909", # CPF de Teste, ao implementar, alterar para(current_user.cpf)
            "phones": [
                {
                    "country": "55",
                    "area": "21",
                    "number": "999999999"
                }       
            ] 
        },

    "items": [
        {
            "reference_id": plano,
            "name": titulo_plano,
            "quantity": 1,
            "unit_amount": valor_centavos
        }
    ],
        "shipping": {
            "address": {
                "street": "Av. PagBank",
                "number": "1000",
                "complement": "Sala 1",
                "locality": "Rio de Janeiro",
                "city": "Rio de Janeiro",
                "region_code": "RJ",
                "country": "BRA",
                "postal_code": "20040002"
            
            }
        },
        "redirect_url": url_for('payments.aprovado', _external=True)
}
    try:
        response = requests.post(PAGBANK_URL, json=payload, headers=headers)
        
        if response.status_code in [200, 201]:
            dados = response.json()
            
            # Pega o link de pagamento
            links = dados.get('links', [])
            link_pagamento = None
            for link in links:
                if link['rel'] == 'pay':
                    link_pagamento = link['href']
                    break
            
            if link_pagamento:
                # SUCESSO: Manda o usuário para o PagBank
                return redirect(link_pagamento)
            else:
                print("JSON PagBank:", dados)
                flash('Erro: PagBank não gerou o link.', 'danger')
        else:
            print(f"Erro PagBank ({response.status_code}):", response.text)
            flash('Erro ao comunicar com o PagBank.', 'danger')

    except Exception as e:
        print("Erro de conexão:", e)
        flash('Erro interno de conexão.', 'danger')

    return redirect(url_for('payments.index'))


@bp.route('/aprovado')
@login_required
def aprovado():
    """
    Rota de retorno do PagBank.
    Recupera quantos dias liberar da sessão.
    """
    dias = session.get('dias_acesso_pendente', 30) # Padrão 30 se falhar
    
    # Lógica de soma de data
    agora = datetime.utcnow()
    if current_user.assinatura_valida_ate and current_user.assinatura_valida_ate > agora:
        current_user.assinatura_valida_ate += timedelta(days=dias)
    else:
        current_user.assinatura_valida_ate = agora + timedelta(days=dias)
    
    db.session.commit()
    
    # Limpa a sessão
    session.pop('dias_acesso_pendente', None)
    
    flash(f'Pagamento aprovado! Você ganhou {dias} dias de acesso Premium.', 'success')
    return redirect(url_for('content.index'))
# Função obrigatória para o Flask carregar o módulo
def init_payments_routes(app):
    app.register_blueprint(bp)