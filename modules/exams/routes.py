# /modules/exams/routes.py
from flask import Blueprint

bp = Blueprint('exams', __name__, url_prefix='/exams')

@bp.route('/')
def list_exams():
    return "Lista de Exames Disponíveis"

@bp.route('/<int:exam_id>/start')
def start_exam(exam_id):
    return f"Iniciando o exame {exam_id}"

def init_exams_routes(app):
    app.register_blueprint(bp)