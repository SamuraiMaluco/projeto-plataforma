import mercadopago # <<< SDK do MP
import os
import json
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from core.extensions import db
from modules.auth.models import User
from .models import Payment
from datetime import datetime, timedelta

bp= Blueprint('payments', __name__, url_prefix='/payments')

#configurando o TOKEN DO MERCADO PAGO
sdk = mercadopago.SDK(os.environ.get('MP_ACCESS_TOKEN') )

#DEFINE OS PREÇOS EM QUESTÃO 
PRECOS = {
    'anual_avista': 456.00,
    'anual_parcelado': 570.00
}

@bp.route('/')
def index():
    #Rota da página de planos
    if current_user.assinatura_valida_ate and current_user.assinatura_valida_ate > datetime.utcnow():
        flash('Você já possui uma assinatura ativa!', 'info')
        return redirect(url_for('core.home'))
    
    return render_template('pagamento.html',
                           plano=request.args.get('plano'))
    
@bp.route('/criar_preferencia', methods=['POST'])
@login_required
def criar_preferencia():
    #Rota criada pelo javascript do pagamento.html para criar uma preferência de pagamento no MP
    #devolve a url de redirect para o frontend
    data = request.get_json()
    plano = data.get('plano')
    
    if plano not in PRECOS:
        return jsonify({'error': 'Plano inválido'}), 400
    
    
    
    amount = PRECOS[plano]
    
    # Obtém o URL base do teu site (ex: http://127.0.0.1:5000)
    # IMPORTANTE: Para o webhook funcionar, isto terá de ser um URL público (ver Passo 2.E)
    base_url = request.url_root 

    # Dados da preferência de pagamento
    preference_data = {
        "items": [
            {
                "title": f"Assinatura Anual - Plano {plano}",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": amount
            }
        ],
        "payer": {
            "email": current_user.email,
        },
        "back_urls": {
            # URLs para onde o usuário é redirecionado após o pagamento
            "success": url_for('payments.pagamento_sucesso', _external=True),
            "failure": url_for('payments.index', _external=True),
            "pending": url_for('payments.index', _external=True)
        },
        "auto_return": "approved", # Só retorna automaticamente se for aprovado
        "notification_url": f"{base_url}payments/mp-webhook", # Onde o MP vai nos avisar
        "external_reference": f"user_id_{current_user.id}_plano_{plano}" # Guardamos o ID do usuário aqui
    }

    try:
        # Cria a preferência de pagamento
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        # Devolve o 'init_point' (URL de pagamento do MP) para o frontend
        return jsonify({
            'init_point': preference['init_point']
        })
    except Exception as e:
        print("Erro ao criar preferência:", e)
        return jsonify({'error': str(e)}), 500


@bp.route('/mp-webhook', methods=['POST'])
def mp_webhook():

    #Esta rota é chamada APENAS pelo Mercado Pago (IPN).
    #É aqui que confirmamos o pagamento e damos o acesso.
  
    data = request.get_json()
    
    try:
        if data.get("type") == "payment":
            payment_id = data.get("data", {}).get("id")
            if not payment_id:
                return "payment_id missing", 400

            # Busca os dados completos do pagamento no MP
            payment_info_response = sdk.payment().get(payment_id)
            payment = payment_info_response["response"]

            if payment["status"] == "approved":
                # Pagamento APROVADO!
                
                # Pega a referência que guardámos (ex: "user_id_123_plano_anual")
                external_reference = payment.get("external_reference")
                if not external_reference or not external_reference.startswith("user_id_"):
                    return "external_reference inválida", 400
                
                # Extrai o ID do usuário
                user_id = int(external_reference.split("_")[2]) 
                
                user = User.query.get(user_id)
                if not user:
                    return "Usuário não encontrado", 404

                # --- LÓGICA DE NEGÓCIO CRÍTICA ---
                # Adiciona 1 ano de acesso ao utilizador
                user.assinatura_valida_ate = datetime.utcnow() + timedelta(days=366)
                
                # Regista o pagamento na nossa tabela `Payment`
                novo_pagamento = Payment(
                    amount=payment["transaction_amount"],
                    status='succeeded',
                    user_id=user_id
                )
                db.session.add(novo_pagamento)
                db.session.add(user)
                db.session.commit()

    except Exception as e:
        print(f"Erro no webhook: {e}")
        db.session.rollback()
        return "webhook error", 500

    return "OK", 200 # Responde OK para o Mercado Pago


@bp.route('/pagamento-sucesso')
@login_required
def pagamento_sucesso():
    #Página para onde o usuário é redirecionado após pagar.
    flash("Pagamento aprovado! Bem-vindo(a)!", "success")
    return redirect(url_for('core.home'))


def init_payments_routes(app):
    app.register_blueprint(bp)
    