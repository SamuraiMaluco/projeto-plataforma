from datetime import datetime
from sqlalchemy import func, and_
from core.extensions import db
from modules.content.models import Lesson, Subject
from .models import LessonProgress, SubjectProgress

class ProgressService:
    @stathicmethod
    def record_lesson_acess(user_id, lesson_id):
        #registra o acesso e retrona o objeto lessonProgress
        progress = LessonProgress.query.filter_by(
            user_id=user_id,
            lesson_id=lesson_id
        ).first()
        
        if not progress:
              progress = SubjectProgress(
                user_id=user_id,
                subject_id=subject_id
            )
        db.session.add(progress)
        progress.completed_lessons = completed
        progress.total_lessons = total
        progress.progress_percentage = (completed / total * 100) if total > 0 else 0
        progress.last_updated = datetime.utcnow()
        
        return progress

    @staticmethod
    def get_user_progress(user_id, subject_id=None):
        """
        #Obtém o progresso consolidado
        Retorna: Dict com estrutura:
            {
                'total': {completed: int, total: int, percentage: float},
                'subjects': [
                    {subject_id: int, name: str, completed: int, total: int, percentage: float}
                ]
            }
        """
        result = {'total': {}, 'subjects': []}
        
        # Progresso geral
        if subject_id:
            # Progresso específico de uma matéria
            progress = SubjectProgress.query.filter_by(
                user_id=user_id,
                subject_id=subject_id
            ).first()
            
            if progress:
                result['total'] = {
                    'completed': progress.completed_lessons,
                    'total': progress.total_lessons,
                    'percentage': progress.progress_percentage
                }
        else:
            # Progresso global
            completed = LessonProgress.query.filter_by(
                user_id=user_id,
                is_completed=True
            ).count()
            
            total = Lesson.query.count()
            
            result['total'] = {
                'completed': completed,
                'total': total,
                'percentage': (completed / total * 100) if total > 0 else 0
            }
            
            # Progresso por matéria
            subjects = Subject.query.all()
            for subject in subjects:
                progress = SubjectProgress.query.filter_by(
                    user_id=user_id,
                    subject_id=subject.id
                ).first()
                
                if progress:
                    result['subjects'].append({
                        'subject_id': subject.id,
                        'name': subject.name,
                        'completed': progress.completed_lessons,
                        'total': progress.total_lessons,
                        'percentage': progress.progress_percentage,
                        'icon': subject.icon
                    })
        
        return result

    @staticmethod
    def get_lesson_status(user_id, lesson_id):
        """
        Verifica status específico de uma aula
        Retorna: Dict com {is_completed: bool, last_accessed: datetime}
        """
        progress = LessonProgress.query.filter_by(
            user_id=user_id,
            lesson_id=lesson_id
        ).first()
        
        return {
            'is_completed': progress.is_completed if progress else False,
            'last_accessed': progress.last_accessed if progress else None
        }
            