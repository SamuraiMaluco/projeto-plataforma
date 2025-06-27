import os
from dotenv import load_dotenv

load_dotenv()

class Config:
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