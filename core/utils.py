import re
import unicodedata
import os
from werkzeug.utils import secure_filename

def validar_senha(senha):
    return (len(senha) >= 8 and
            re.search(r'[0-9]', senha) and
            re.search(r'[A-Z]', senha) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', senha))

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = re.sub(r'[^\w\s-]', '', text.lower().strip())
    return re.sub(r'[-\s]+', '-', text)

def allowed_file(filename, filetype, config):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config['ALLOWED_EXTENSIONS'].get(filetype, [])