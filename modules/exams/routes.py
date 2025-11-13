#estabelecendo rotas para o módulo de exames
from flask import Blueprint

bp = Blueprint('exams', __name__, url_prefix='/exams')

@bp.route('/')
def list_exams():
    return "Lista de Exames Disponíveis"

def init_exams_routes(app):
    app.register_blueprint(bp)