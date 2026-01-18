from core.extensions import db
from modules.content.models import LessonProgress, SubjectProgress, Module, Lesson
from flask_login import current_user

class ProgressService:

    @staticmethod
    def get_user_progress_summary(user_id):
        #retorna o progresso geral do usuário em todos os módulos

        total_lessons = Lesson.query.count()

        completed_lessons = LessonProgress.query.filter_by(
            user_id=user_id,
            completed=True
        ).count()

        #calculo de porcentagem
        if total_lessons > 0:
            percentage = int((completed_lessons / total_lessons) * 100)
        else:
            percentage = 0

        return {
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "percentage": int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0
        }

    @staticmethod
    def get_module_progress(user_id, module_id):
        """Calcula a porcentagem de conclusão de um Módulo (antigo Content)"""
        module = Module.query.get(module_id)
        if not module:
            return 0
            
        total_lessons = module.lessons.count()
        if total_lessons == 0:
            return 0
            
        # Conta quantas aulas desse módulo o usuário completou
        completed_lessons = LessonProgress.query.join(Lesson).filter(
            LessonProgress.user_id == user_id,
            LessonProgress.completed == True,
            Lesson.module_id == module_id
        ).count()
        
        return int((completed_lessons / total_lessons) * 100)

    @staticmethod
    def mark_lesson_completed(user_id, lesson_id):
        progress = LessonProgress.query.filter_by(
            user_id=user_id, 
            lesson_id=lesson_id
        ).first()

        if not progress:
            progress = LessonProgress(user_id=user_id, lesson_id=lesson_id, completed=True)
            db.session.add(progress)
        else:
            progress.completed = True
            progress.updated_at = db.func.now()
        
        db.session.commit()
        return True