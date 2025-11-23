# /modules/progress/services.py

from datetime import datetime
from core.extensions import db
# Importamos os modelos corretos de conteúdo e progresso
from modules.content.models import Lesson, Content
from .models import LessonProgress, SubjectProgress

class ProgressService:
    @staticmethod
    def complete_lesson(user_id, lesson_id):
        """
        Esta função combina a sua lógica de 'salvar_progresso'.
        Ela encontra ou cria o progresso da lição, marca como concluída,
        e depois atualiza o progresso geral da matéria.
        """
        # (O seu código existente de complete_lesson continua aqui...)
        # ...
        # ...
        db.session.commit()
        return lesson_progress, subject_progress


    # --- FUNÇÃO ADICIONADA ---
    @staticmethod
    def get_user_progress_summary(user_id):
        """
        Calcula o progresso total do usuário para o dashboard.
        """
        # Conta o total de aulas concluídas pelo usuário
        completed_lessons = LessonProgress.query.filter_by(
            user_id=user_id, 
            is_completed=True
        ).count()

        # Conta o total de aulas existentes na plataforma
        total_lessons = Lesson.query.count()
        
        if total_lessons > 0:
            percentage = round((completed_lessons / total_lessons) * 100)
        else:
            percentage = 0
        
        return {
            'completed_lessons': completed_lessons,
            'total_lessons': total_lessons,
            'completion_percentage': percentage
        }