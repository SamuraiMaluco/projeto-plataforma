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
        # Encontra ou cria o registo de progresso para a lição específica
        lesson_progress = LessonProgress.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()

        if not lesson_progress:
            lesson_progress = LessonProgress(user_id=user_id, lesson_id=lesson_id)
            db.session.add(lesson_progress)
        
        # Marca a lição como concluída e atualiza as datas
        lesson_progress.is_completed = True
        lesson_progress.last_accessed = datetime.utcnow()
        lesson_progress.completion_date = datetime.utcnow()

        # Atualiza o progresso agregado da matéria
        lesson = Lesson.query.get(lesson_id)
        if not lesson:
            raise Exception("Lição não encontrada")
        
        subject_id = lesson.content.subject_id
        
        # Conta o total de lições na matéria
        total_lessons_in_subject = Lesson.query.join(Content).filter(Content.subject_id == subject_id).count()

        # Conta as lições concluídas pelo utilizador nesta matéria
        completed_lessons_count = db.session.query(LessonProgress).join(Lesson).join(Content).filter(
            LessonProgress.user_id == user_id,
            Content.subject_id == subject_id,
            LessonProgress.is_completed == True
        ).count()

        # Encontra ou cria o registo de progresso para a matéria
        subject_progress = SubjectProgress.query.filter_by(user_id=user_id, subject_id=subject_id).first()

        if not subject_progress:
            subject_progress = SubjectProgress(user_id=user_id, subject_id=subject_id)
            db.session.add(subject_progress)

        # Atualiza os valores do progresso da matéria
        subject_progress.completed_lessons = completed_lessons_count
        subject_progress.total_lessons = total_lessons_in_subject
        subject_progress.progress_percentage = (completed_lessons_count / total_lessons_in_subject * 100) if total_lessons_in_subject > 0 else 0
        subject_progress.last_updated = datetime.utcnow()

        db.session.commit()
        return lesson_progress, subject_progress