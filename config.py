import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://th:Samurai3@localhost:5432/study_db_v2'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600
    }
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {
        'video': ['mp4', 'mov', 'avi'],
        'audio': ['mp3', 'wav', 'ogg'],
        'image': ['jpg', 'jpeg', 'png', 'gif'],
        'document': ['pdf', 'docx', 'txt']
    }
    CRON_API_KEY = os.getenv('CRON_API_KEY')