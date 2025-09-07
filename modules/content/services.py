# /modules/content/services.py

from sqlalchemy.orm import joinedload
# Importamos os nossos modelos padronizados
from .models import Subject, Content

class ContentService:
    @staticmethod
    def get_content_by_subject(subject_id):
        """Busca todos os conteúdos de uma matéria específica."""
        # Usamos os nomes corretos: Content e subject_id
        return Content.query.filter_by(subject_id=subject_id).all()

    @staticmethod
    def get_all_subjects_with_content():
        """
        Busca todas as matérias e já carrega os seus respectivos conteúdos 
        para evitar múltiplas queries na base de dados (melhor performance).
        """
        # Usamos os nomes corretos: Subject e a relação 'contents'
        return Subject.query.options(joinedload(Subject.contents)).all()