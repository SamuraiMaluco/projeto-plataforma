from core.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


class Exam(db.Model):
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # in minutes
    passing_score = db.Column(db.Integer, default=70)
    is_active = db.Column(db.Boolean, default=True)
    available_from = db.Column(db.DateTime)
    available_to = db.Column(db.DateTime)
    def __repr__(self):
        return f'<Simulado {self.titulo}>'

class ExamQuestion(db.Model):
    __tablename__ = 'exam_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='multiple_choice')
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(10), default='medium')
    
    # Relacionamentos
    exam = db.relationship('Exam', back_populates='questions')
    options = db.relationship('QuestionOption', back_populates='question')

    def __repr__(self):
        return f'<Questao {self.id}>'

class QuestionOption(db.Model):
    __tablename__ = 'question_options'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('exam_questions.id'))
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer)
    def __repr__(self):
        return f'<Alternativa {self.letra} da Questão {self.questao_id}>'

# Tabela de associação muitos-para-muitos
simulado_questoes = db.Table('simulado_questoes',
    db.Column('simulado_id', db.Integer, db.ForeignKey('simulados.id', ondelete='CASCADE'), primary_key=True),
    db.Column('questao_id', db.Integer, db.ForeignKey('questoes.id', ondelete='CASCADE'), primary_key=True),
    db.Column('ordem', db.Integer),
    db.Column('peso', db.Numeric(3,2), default=1.00)
)

class TentativaSimulado(db.Model):
    __tablename__ = 'tentativas_simulado'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    simulado_id = db.Column(db.Integer, db.ForeignKey('simulados.id'))
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime)
    tempo_gasto = db.Column(db.Integer)  # Em segundos
    pontuacao = db.Column(db.Numeric(5,2))
    concluido = db.Column(db.Boolean, default=False)
    
    # Relacionamentos
    usuario = db.relationship('User', backref='tentativas_simulado')
    respostas = db.relationship('RespostaUsuario', backref='tentativa', lazy='dynamic')

    def __repr__(self):
        return f'<Tentativa {self.id} do Simulado {self.simulado_id}>'

class RespostaUsuario(db.Model):
    __tablename__ = 'respostas_usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    tentativa_id = db.Column(db.Integer, db.ForeignKey('tentativas_simulado.id', ondelete='CASCADE'))
    questao_id = db.Column(db.Integer, db.ForeignKey('questoes.id'))
    alternativa_id = db.Column(db.Integer, db.ForeignKey('alternativas.id'))
    resposta_dissertativa = db.Column(db.Text)
    tempo_gasto = db.Column(db.Integer)  # Em segundos
    correta = db.Column(db.Boolean)
    data_resposta = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    alternativa = db.relationship('Alternativa')

    def __repr__(self):
        return f'<Resposta {self.id} da Questão {self.questao_id}>'

class DesempenhoMateria(db.Model):
    __tablename__ = 'desempenho_materia'
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), primary_key=True)
    total_questoes = db.Column(db.Integer, default=0)
    acertos = db.Column(db.Integer, default=0)
    percentual_acerto = db.Column(db.Numeric(5,2))
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    usuario = db.relationship('User', backref='desempenhos')
    materia = db.relationship('Materia', backref='desempenhos')

    def __repr__(self):
        return f'<Desempenho do usuário {self.usuario_id} em {self.materia_id}>'

def init_exams_models():
    """Cria as tabelas específicas do módulo de simulados"""
    db.create_all()