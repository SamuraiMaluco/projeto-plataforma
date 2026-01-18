from core.extensions import db
import re

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True) # Ex: /matematica
    icon = db.Column(db.String(50)) # Ex: 'calculator'
    description = db.Column(db.Text)
    
    # Mudamos de 'contents' para 'modules' para ficar mais claro (Capítulos)
    modules = db.relationship('Module', backref='subject', lazy='dynamic')
    
    # Mantendo relação com progresso (se você tiver essa tabela criada)
    user_progress = db.relationship('SubjectProgress', back_populates='subject', lazy='dynamic')

class Module(db.Model):
    """ Antigo 'Content'. Agora chamamos de Módulo/Capítulo para organizar melhor """
    __tablename__ = 'modules'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    order = db.Column(db.Integer, default=0)
    
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    
    # Relacionamento com as aulas
    lessons = db.relationship('Lesson', backref='module', lazy='dynamic')

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    order = db.Column(db.Integer, default=0)
    is_free = db.Column(db.Boolean, default=False) # Se é aula grátis ou paga


    
    # --- ESTRUTURA HÍBRIDA (VÍDEO + ÁUDIO + PDF + TEXTO) ---
    # Agora temos campos separados para cada tipo de mídia
    
    # 1. Vídeo (Geralmente link do Youtube/Vimeo/Panda)
    video_url = db.Column(db.String(500), nullable=True) 
    
    # 2. Arquivos de Upload (Salvos na pasta static/uploads)
    audio_file = db.Column(db.String(255), nullable=True) # Caminho do MP3
    pdf_file = db.Column(db.String(255), nullable=True)   # Caminho do PDF
    
    # 3. Conteúdo Escrito (Texto rico / HTML)
    content_text = db.Column(db.Text, nullable=True) 
    
    # Extras
    thumbnail_url = db.Column(db.String(500)) # Capa da aula
    duration = db.Column(db.Integer) # Duração em minutos (para mostrar no card)
    # ----------------------------------

    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    
    # Mantendo progresso
    user_progress = db.relationship('LessonProgress', back_populates='lesson', lazy='dynamic')

    @property
    def embed_video_url(self):
        #transforma o link do video em embed
        if not self.video_url:
            return None

        # Regex poderosa para achar o ID do vídeo (funciona com youtu.be, watch?v=, embed/, etc)
        # Fonte: https://stackoverflow.com/questions/34833232/get-youtube-video-id-from-url-with-python-and-regex
        regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(regex, self.video_url)

        if match:
            video_id = match.group(1)
            # Retorna o link de embed com parâmetros para ficar mais limpo (sem vídeos relacionados de outros canais)
            return f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1"
        
        return self.video_url # Se não achar ID, retorna o link original (fallback)

# --- CLASSES DE PROGRESSO (Mantenha se já existiam no seu projeto) ---
class SubjectProgress(db.Model):
    __tablename__ = 'subject_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    progress_percent = db.Column(db.Float, default=0.0)
    subject = db.relationship('Subject', back_populates='user_progress')
    user = db.relationship('User', back_populates='subject_progress')

class LessonProgress(db.Model):
    __tablename__ = 'lesson_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=db.func.now())

    lesson = db.relationship('Lesson', back_populates='user_progress')

    user = db.relationship('User', back_populates='lesson_progress')