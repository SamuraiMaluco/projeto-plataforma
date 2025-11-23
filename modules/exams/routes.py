# estabelecendo rotas para o módulo de exames
from flask import Blueprint
# --- IMPORTS ADICIONADOS ---
# Precisamos importar os modelos aqui para que o SQLAlchemy
# "saiba" que eles existem quando o app for iniciado.
from .models import Exam, Question, Option, ExamAttempt
# --- FIM DOS IMPORTS ---

bp = Blueprint('exams', __name__, url_prefix='/exams')

@bp.route('/')
def list_exams():
    return "Lista de Exames Disponíveis"

def init_exams_routes(app):
    app.register_blueprint(bp)