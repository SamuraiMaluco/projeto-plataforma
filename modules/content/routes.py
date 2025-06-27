from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from core.decorators import login_required
from modules.content.models import Materia, Conteudo
from modules.auth.models import User

bp = Blueprint('content', __name__, url_prefix='/content')

@bp.route('/aulas')
@login_required
def aulas():
    user = User.query.filter_by(email=session['email']).first()
    materias = Materia.query.filter_by(visivel=True).all()
    ramos = [r[0] for r in db.session.query(Materia.ramo).distinct().all() if r[0]]
    niveis = [n[0] for n in db.session.query(Materia.nivel).distinct().all() if n[0]]
    
    return render_template('content/aulas.html',
                        user=user,
                        materias=materias,
                        ramos=ramos,
                        niveis=niveis,
                        assinatura_ativa=user.assinatura_valida_ate and user.assinatura_valida_ate > datetime.now())

@bp.route('/materia/<int:materia_id>')
@login_required
def materia(materia_id):
    materia = Materia.query.get_or_404(materia_id)
    conteudos = Conteudo.query.filter_by(materia_id=materia_id).order_by(Conteudo.ordem).all()
    return render_template('content/materia.html',
                         materia=materia,
                         conteudos=conteudos)

@bp.route('/conteudo/<int:conteudo_id>')
@login_required
def ver_conteudo(conteudo_id):
    user = User.query.filter_by(email=session['email']).first()
    conteudo = Conteudo.query.get_or_404(conteudo_id)
    
    if conteudo.pago and not (user.assinatura_valida_ate and user.assinatura_valida_ate > datetime.now()):
        flash('Este conteúdo requer assinatura ativa', 'warning')
        return redirect(url_for('payments.pagamento'))
    
    return render_template('content/ver_conteudo.html',
                         conteudo=conteudo)