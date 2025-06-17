import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import re #módulo para validar senha
from werkzeug.utils import secure_filename
import os
import logging
from logging.handlers import RotatingFileHandler
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from flask_login import LoginManager, login_required, current_user, UserMixin
from functools import wraps
from flask import redirect, url_for, flash
from slugify import slugify
from flask import abort





app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_key') 
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://th:Samurai3@localhost:5432/study_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CRON_API_KEY'] = 'sua_chave_secreta_aqui'
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {
    'video': ['mp4', 'mov', 'avi'],
    'audio': ['mp3', 'wav', 'ogg'],
    'image': ['jpg', 'jpeg', 'png', 'gif'],
    'document': ['pdf', 'docx', 'txt']
}
# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Rota para redirecionar se não estiver logado





# configurações específicas
def admin_required(func):
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash('Acesso restrito ao administrador.', 'danger')
            return redirect(url_for('home'))  # ou uma rota de acesso negado
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:  # Mude de 'user_id' para 'email' para consistência
            flash('Por favor, faça login para acessar esta página', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica se o usuário está logado
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta área', 'warning')
            return redirect(url_for('login', next=request.url))
        user = User.query.get(session['user_id'])
        # Verifica se o usuário existe
        user = User.query.get(session['user_id'])
        if not user:
            flash('Usuário não encontrado', 'danger')
            session.pop('user_id', None)
            return redirect(url_for('login'))
        
        # Verifica se é admin
        if not user.is_admin:
            flash('Acesso permitido apenas para administradores', 'danger')
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename, filetype):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'][filetype]

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    filetype = request.form.get('filetype', 'document')
    
    if file.filename == '':
        return jsonify({'error': 'Nome de arquivo vazio'}), 400
    
    if file and allowed_file(file.filename, filetype):
        filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filetype + 's', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        
        # Retorna URL relativa para armazenar no banco
        return jsonify({
            'url': f"/static/uploads/{filetype}s/{filename}",
            'filename': filename
        })
    
    return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
def slugify(text):
    import re
    import unicodedata
    
    # Remove acentos e caracteres especiais
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    
    # Converte para minúsculas e substitui espaços/não-alfanuméricos
    text = re.sub(r'[^\w\s-]', '', text.lower().strip())
    text = re.sub(r'[-\s]+', '-', text)
    
    return text

def carregar_materias():
    caminho_json = os.path.join(os.path.dirname(__file__), 'data', 'materias.json')  # Corrigido os.path.join
    with open(caminho_json, 'r', encoding='utf-8') as f:
        return json.load(f)
    
     
def  __init__(self, nome, slug, descricao, icone, ordem_exibicao, estrutura=None):
    self.nome = nome
    self.slug = slug
    self.descricao = descricao
    self.icone = icone
    self.ordem_exibicao = ordem_exibicao
    self.estrutura = estrutura or{}
    
    
def to_dict(self):
    return{
        'id': self.id,
            'nome': self.nome,
            'slug': self.slug,
            'descricao': self.descricao,
            'icone': self.icone,
            'ordem_exibicao': self.ordem_exibicao,
            'estrutura': self.estrutura
    }
    
    
    
    
    
    

#configurando logs
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)  
app.logger.addHandler(handler)  

# Handlers de erro
@app.errorhandler(404)
def not_found_error(error):  
    app.logger.error(f'Erro 404: {error}')
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_error(error):  #
    db.session.rollback()
    app.logger.error(f'Erro 500: {error}', exc_info=True)
    return render_template('error/500.html'), 500



class User(db.Model, UserMixin):
    __tablename__='users'
    is_admin = db.Column(db.Boolean, default=False)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    assinatura_valida_ate = db.Column(db.DateTime)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    plano_assinatura = db.Column(db.String(20))
    parcelas_restantes = db.Column(db.Integer, default=0)
    valor_parcela = db.Column(db.Float)
    proximo_pagamento = db.Column(db.DateTime)
    data_assinatura = db.Column(db.DateTime)
    parcelas_restantes = db.Column(db.Integer)
    
    
def create_admin():
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@dev.com',
                senha=generate_password_hash('@admin123'),
                is_admin=True
            )    
            db.session.add(admin)
            db.session.commit()
            print('admin criado com sucesso!')
        else:
            print('admin já existe!')
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class Materia(db.Model):
    __tablename__='materias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column (db.String(100), nullable=False)
    ramo = db.Column(db.String(50)) # os tipos de direito(constitucional, penal, etc)
    nivel = db.Column(db.String(20)) # fácil, médio e difícil
    icone = db.Column(db.String(30)) #gravel, balance-scale
    visivel = db.Column(db.Boolean, default=True)
    estrutura = db.Column(db.JSON, nullable = True)
    
    #rel com conteudo
    conteudos = db.relationship('Conteudo', backref='materia', lazy='select', order_by='Conteudo.ordem')
        
class Conteudo(db.Model):
    __tablename__ = 'conteudos'
    id = db.Column(db.Integer, primary_key=True)
    titulo =db.Column(db.String(100), nullable=False)
    tipo =db.Column(db.String(20), nullable=False) #audio/pdf/quiz...
    tipo_media = db.Column(db.String(20))
    url = db.Column(db.String(255), nullable=False)
    duracao = db.Column(db.Integer)
    duracao_segundos = db.Column(db.Integer)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    ordem = db.Column(db.Integer, nullable=False)
    pago = db.Column(db.Boolean, default=False)
    conteudo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    dados = db.Column(db.JSON, nullable=False)
    
    
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'ordem': self.ordem,
            'dados': self.dados
        }
    
    
    #database do administrador
class Capitulo(db.Model):
    __tablename__ = 'capitulos'
    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    conteudo_texto = db.Column(db.Text)
    media_url = db.Column(db.String(255))
    tipo_media = db.Column(db.String(20))  # video, audio, pdf
    ordem = db.Column(db.Integer)  # 1 a 4
    
    
    class QuestaoAula(db.Model):
        __tablename__ = 'questoes_aula'
    id = db.Column(db.Integer, primary_key=True)
    capitulo_id = db.Column(db.Integer, db.ForeignKey('capitulos.id'), nullable=False)
    enunciado = db.Column(db.Text, nullable=False)
    alternativas = db.Column(db.JSON, nullable=False)  # {'A': '...', 'B': '...', ...}
    correta = db.Column(db.String(1), nullable=False)  # 'A', 'B', etc.
    
    
    class QuestaoAula(db.Model):
        __tablename__ = 'questoes_aula'
    id = db.Column(db.Integer, primary_key=True)
    capitulo_id = db.Column(db.Integer, db.ForeignKey('capitulos.id'), nullable=False)
    enunciado = db.Column(db.Text, nullable=False)
    alternativas = db.Column(db.JSON, nullable=False)  # {'A': '...', 'B': '...', ...}
    correta = db.Column(db.String(1), nullable=False)  # 'A', 'B', etc.
    explicacao = db.Column(db.Text)  # explicação opcional da resposta
    criada_em = db.Column(db.DateTime, default=datetime.utcnow)

# Opcional: para simulados, um banco separado
class QuestaoSimulado(db.Model):
    __tablename__ = 'questoes_simulado'
    id = db.Column(db.Integer, primary_key=True)
    origem = db.Column(db.String(100))  # concurso, banca, ano
    enunciado = db.Column(db.Text, nullable=False)
    alternativas = db.Column(db.JSON, nullable=False)
    correta = db.Column(db.String(1), nullable=False)
    nivel = db.Column(db.String(20))  # fácil, médio, difícil
    criada_em = db.Column(db.DateTime, default=datetime.utcnow)

    
    
    #fim do adm
    
    
    
class Transacao(db.Model):
    __tablename__='transacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    valor = db.Column(db.Float)
    plano = db.Column(db.String(20))
    data = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20))
    metodo = db.Column(db.String(20))   
    usuario = db.relationship('User', backref=db.backref('transacoes', lazy=True))
        
        
        
        
        #funções auxiliares
def validar_senha(senha):
    # verifica se tem pelo menos 8 caracteres
    if len(senha) < 8:
        return False
    
    # verifica se tem pelo menos um número
    if not re.search(r'[0-9]', senha):
        return False
    
    # verifica se tem pelo menos uma letra maiúscula
    if not re.search(r'[A-Z]', senha):
        return False
    
    # verifica se tem pelo há pelo menos um caracter especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return False   
    
    #Se todos os critérios forem atendidos, a senha é válida
    return True

        




@app.route('/')
def home():
    if 'email' in session:  
        user = User.query.filter_by(email=session['email']).first()  
        if user:
            
            if session.get('primeira_visita', True):
                session['primeira_visita'] = False
                mensagem = 'Seja muito bem-vindo'
            else:
                mensagem = 'Bem-vindo de volta'
                
            #verificar a assinatura do usuário
            assinatura_ativa = user.assinatura_valida_ate and user.assinatura_valida_ate > datetime.now()
        
            return render_template('home.html', email=user.email, username=user.username, mensagem=mensagem, assinatura=assinatura_ativa)
        
        
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash('Por favor, preencha os campos abaixo!', 'error')
            return redirect(url_for('login'))

        email = email.strip()
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.senha, senha):
            session['email'] = email
            next_page = request.args.get('next') or url_for('home')
            return redirect(next_page)
        else:
            flash('E-mail ou senha incorretos!', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

    
@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

# Gestão de Matérias
@app.route('/admin/materias')
@admin_required
def admin_materias():
    materias = Materia.query.order_by(Materia.ordem_exibicao).all()
    return render_template('admin/materias/listar.html', materias=materias)

@app.route('/admin/materias/nova', methods=['GET', 'POST'])
@admin_required
def nova_materia():
    if request.method == 'POST':
        materia = Materia(
            nome=request.form['nome'],
            slug=slugify(request.form['nome']),
            descricao=request.form['descricao'],
            icone=request.form['icone'],
            ordem_exibicao=request.form.get('ordem', 0)
        )
        db.session.add(materia)
        db.session.commit()
        return redirect(url_for('admin_materias'))
    
    return render_template('admin/materias/editar.html')

# Gestão de Conteúdos
@app.route('/admin/conteudos')
@admin_required
def admin_conteudos():
    conteudos = Conteudo.query.join(Materia).order_by(
        Materia.ordem_exibicao, 
        Conteudo.ordem
    ).all()
    return render_template('admin/conteudos/listar.html', conteudos=conteudos)

@app.route('/admin/conteudos/novo', methods=['GET', 'POST'])
@admin_required
def novo_conteudo():
    if request.method == 'POST':
        conteudo = Conteudo(
            titulo=request.form['titulo'],
            tipo=request.form['tipo'],
            materia_id=request.form['materia_id'],
            ordem=request.form.get('ordem', 0),
            pago='pago' in request.form,
            # ... outros campos
        )
        db.session.add(conteudo)
        db.session.commit()
        return redirect(url_for('admin_conteudos'))
    
    materias = Materia.query.filter_by(visivel=True).all()
    return render_template('admin/conteudos/editar.html', materias=materias)



@app.route('/logout')
def logout():
    # Remove o email da sessão
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # área de cadastro
    if request.method =='POST':
        username = request.form.get('username')
        email = request.form.get('email')
        senha = request.form.get('senha')
        print(f"Dados do formulário: {username}, {email}, {senha}")
        
        
        if not username or not email or not senha:
            flash('Por favor, preencha os campos abaixo', 'error')
            return render_template('register.html')
        
         # validação da senha    
        if not validar_senha(senha):
            flash('A senha deve conter pelo menos 8 caracteres, um número, uma letra maiúscula e um caracter especial', 'error')
            return redirect(url_for('register'))
        
        username = username.strip()
        email = email.strip()
            # verifica se o nome ou email já existe no banco de dados
        if User.query.filter_by(username=username).first():
                flash('Este nome já existe!', 'error')
                return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
                flash('Este email já foi cadastrado!', 'error')
                return redirect(url_for('register'))
            # criar um novo user
        hashed_senha = generate_password_hash(senha)
        print(f"Senha criptografada: {hashed_senha}")
            
        new_user = User(username=username, email=email, senha=hashed_senha) 
        try:
            db.session.add(new_user)
            db.session.commit()
            print("Usuário cadastrado no banco de dados")
            flash('Cadastro concluído!', 'sucesso')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar usuário: {e}")
            flash('Ocorreu um erro ao cadastrar o usuário.', 'error')
            return redirect(url_for('register'))
    return render_template('register.html')


@app.route("/aulas")
@login_required  # Adicione este decorator se necessário
def aulas():
    #Rota principal para exibição das aulas
    try:
        user = User.query.filter_by(email=session['email']).first()
        if not user:
            return redirect(url_for('logout'))

        materias = Materia.query.options(
            db.joinedload(Materia.conteudos)
        ).filter(Materia.visivel == True).all()
        
        ramos = [r[0] for r in db.session.query(Materia.ramo).distinct().all() if r[0]]
        niveis = [n[0] for n in db.session.query(Materia.nivel).distinct().all() if n[0]]
        materias = Materia.query.options(joinedload(Materia.conteudos)).filter_by(visivel=True).all()
        return render_template('aulas.html',
                            user=user,
                            materias=materias,
                            ramos=ramos,
                            niveis=niveis,
                            assinatura_ativa=user.assinatura_valida_ate and user.assinatura_valida_ate > datetime.now())
    except Exception as e:
        app.logger.error(f"Erro na rota /aulas: {str(e)}")
        flash('Erro ao carregar aulas', 'error')
        return redirect(url_for('home'))

@app.route('/simulados')
@login_required
def simulados():
    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return redirect(url_for('logout'))

    return render_template('simulados.html',
                        user=user,
                        assinatura_ativa=user.assinatura_valida_ate and user.assinatura_valida_ate > datetime.now())
    
@app.route('/materias')
def materias():
    # Verifica se o usuário está logado
    
    if 'email' not in session:
        return redirect(url_for('login'))

    # Busca o usuário autenticado
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return redirect(url_for('logout'))

    # Agrupa matérias por ramo
    materias_por_ramo = db.session.query(Materia.ramo, db.func.array_agg(Materia)).group_by(Materia.ramo).all()
    materias_por_ramo_dict = {ramo: materias for ramo, materias in materias_por_ramo}
    
    return render_template('materias.html',
                           user=user,
                           materias_por_ramo=materias_por_ramo_dict,
                           assinatura_ativa=user.assinatura_valida_ate and user.assinatura_valida_ate > datetime.now())




@app.route('/materia/<int:materia_id>', methods=['GET'])
def get_materia(materia_id):
    # Função que retorna a matéria em formato JSON
    materia = Materia.query.get(materia_id)
    if materia:
        return jsonify(materia.to_dict())
    else:
        return jsonify({'error': 'Matéria não encontrada'}), 404


@app.route('/materia/detalhes/<int:materia_id>', methods=['GET'])
def show_materia(materia_id):
    # Função que renderiza a página HTML com a matéria
    return render_template('materia.html', materia_id=materia_id)


@app.route('/materia/conteudos/<int:materia_id>', methods=['GET'])
def conteudos_materia(materia_id):
    # Função para exibir os conteúdos relacionados à matéria
    if 'email' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return redirect(url_for('logout'))
    
    materia = Materia.query.get_or_404(materia_id)
    conteudos = Conteudo.query.filter_by(materia_id=materia_id).order_by(Conteudo.ordem).all()

    return render_template('conteudos_materia.html',
                           user=user,
                           materia=materia,
                           conteudos=conteudos,
                           assinatura_ativa=user.assinatura_valida_ate and user.assinatura_valida_ate > datetime.now())
    
    
    
    
    
    
def show_materia(id):
    return render_template('materia.html', materia_id=id)
def conteudos_materia(materia_id):
    if'email' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return redirect(url_for('logout'))
    
    materia = Materia.query.get_or_404(materia_id)
    conteudos = Conteudo.query.filter_by(materia_id=materia_id).order_by(Conteudo.ordem).all()
    return render_template('conteudos_materia.html',
                           user=user,
                            materia=materia,
                            conteudos=conteudos,
                            assinatura_ativa=user.assinatura_valida_ate and user.assinatura_valida_ate > datetime.now())
    

@app.route('/conteudo/<int:conteudo_id>')
def ver_conteudo(conteudo_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return redirect(url_for('logout'))
    
    conteudo = Conteudo.query.get_or_404(conteudo_id)
    
    # Verificar se o conteúdo é pago e se o usuário tem assinatura
    if conteudo.pago and not (user.assinatura_valida_ate and user.assinatura_valida_ate > datetime.now()):
        flash('Este conteúdo requer assinatura ativa', 'warning')
        return redirect(url_for('pagamento'))
    
    return render_template('ver_conteudo.html',
                         user=user,
                         conteudo=conteudo)






@app.route('/progresso')
def progresso():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email=session['email']).first()
    return render_template('progresso.html',
                        username=user.username,
                        assinatura=user.assinatura_valida_ate and user.assinatura_valida_ate > datetime.now())





@app.route('/conteudo/adicionar', methods=['GET', 'POST'])
def adicionar_conteudo():
    if request.method == 'POST':
        # Processar formulário
        titulo = request.form['titulo']
        tipo = request.form['tipo']
        materia_id = request.form['materia_id']
        ordem = request.form['ordem']
        pago = 'pago' in request.form
        ordem = request.form['ordem']
   
        
        # Configurações específicas por tipo
        if tipo == 'video':
            url = request.form['video_url']
            tipo_media = url.split('.')[-1]
            duracao_segundos = int(request.form['duracao'])
            transcricao = request.form['transcricao']
            thumbnail = request.form.get('thumbnail_url', '')
        elif tipo == 'audio':
            url = request.form['audio_url']
            tipo_media = url.split('.')[-1]
            duracao_segundos = int(request.form['duracao'])
            transcricao = request.form['transcricao']
        elif tipo == 'imagem':
            url = request.form['imagem_url']
            tipo_media = url.split('.')[-1]
            conteudo = request.form['descricao_imagem']
            
        
        novo_conteudo = Conteudo(
            titulo=titulo,
            tipo=tipo,
            tipo_media=tipo_media,
            url=url,
            url_thumbnail=thumbnail if tipo == 'video' else None,
            duracao=duracao_segundos // 60 if tipo in ['video', 'audio'] else None,
            duracao_segundos=duracao_segundos if tipo in ['video', 'audio'] else None,
            materia_id=materia_id,
            ordem=ordem,
            pago=pago,
            conteudo=conteudo if tipo == 'imagem' else None,
            transcricao=transcricao if tipo in ['video', 'audio'] else None
        )
        
        db.session.add(novo_conteudo)
        db.session.commit()
        flash('Conteúdo adicionado com sucesso!', 'success')
        return redirect(url_for('conteudos_materia', materia_id=materia_id))
    
    materias = Materia.query.all()
    return render_template('adicionar_conteudo.html', materias=materias)
    
    
    
    
    #área de pagamento
    
@app.route('/pagamento', methods=['GET','POST'])
    
@login_required
def pagamento():
    #ver autenticaçao
    user = User.query.filter_by(email=session['email']).first()
            #aqui é o money playboy
            
    PLANOS = {
            
            #plano mensal com fidelidade anual
            
        'anual_parcelado':{
            'valor_parcela': 47.50,
            'parcelas': 12,
            'valor_total': 570,
            'tipo': 'anual_parcelado',
            'descricao': 'Parcelado (12x)'
        
        },
        
            #total com 20%
            
        'anual_avista' : {
            'valor' : 456,
            'tipo' : 'anual_avista',
            'descricao': 'Anual à Vista (Desconto)',
            'economia': 114 #570 - 456
            
            
        }       
        
    }






    if request.method == 'POST':
        #processar pagamento
        plano_escolhido = request.form.get('plano')
        try:
            if plano_escolhido== 'anual_parcelado':
               #imp plano anual parcelado
                pass
                #logica da primeira parcela de 47.50
                
            elif plano_escolhido == 'anual_avista':
                # Lógica para processar pagamento único de R$456,00
                pass
            
            db.session.commit()
            flash('Assinatura ativada com sucesso!', 'success')
            return redirect(url_for('painel_usuario'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erro no pagamento: {str(e)}")
            flash('Erro ao processar pagamento', 'danger')
            return redirect(url_for('pagamento'))

    return render_template('pagamento.html',
                        user=user,
                        planos=PLANOS,
                        hoje=datetime.now().strftime('%Y-%m-%d'),
                        assinatura_ativa=user.assinatura_valida_ate and user.assinatura_valida_ate > datetime.now())
        
@app.route('/processar-parcelas' , methods=['POST'])
def processar_parcelas():
    #verificar
    if request.headers.get('X-API-KEY') != app.config['CRON_API_KEY']:
        abort(401)
        
        
    #buscar caloteiro
    usuarios = User.query.filter(
        User.plano_assinatura == 'anual_parcelado',
        User.parcelas_restantes > 0,
        User.proximo_pagamento <= datetime.now()
    ).all()
    
    for user in usuarios:
        try:
            # Simular cobrança da parcela
            valor_cobrado = user.valor_parcela
            
            # Aqui você faria a integração real com o gateway de pagamento
            # Exemplo: response = gateway.cobrar_parcela(user, valor_cobrado)
            
            # Atualizar dados do usuário
            user.parcelas_restantes -= 1
            user.proximo_pagamento = datetime.now() + timedelta(days=30)
            db.session.commit()
            
            # Registrar a transação
            transacao = Transacao(
                user_id=user.id,
                valor=valor_cobrado,
                data=datetime.now(),
                tipo='parcela_recorrente',
                status='aprovado'
            )
            db.session.add(transacao)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erro ao processar parcela para usuário {user.id}: {str(e)}")
            # Implementar lógica de retentativa ou notificação
    
    return jsonify({
        'status': 'success',
        'parcelas_processadas': len(usuarios),
        'data_processamento': datetime.now().isoformat()
    })
    
    
@app.route('/pagamento-sucesso')
@login_required
def pagamento_sucesso():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('pagamento_sucesso.html', user=user)
        
    
    
    
    
    
    
@app.route('/listar-rotas')
def listar_rotas():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': sorted(rule.methods),
            'path': str(rule)
        })
    return jsonify({'routes': routes})
    
    
    
    
    

if __name__ == '__main__':
    create_admin()
    with app.app_context(): 
        db.create_all()
    app.run(debug=True, port=5000)
