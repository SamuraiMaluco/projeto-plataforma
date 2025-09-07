# /core/utils.py
# Funções de utilidade geral para o projeto.
import re
import unicodedata

def validar_senha(senha):
    return (len(senha) >= 8 and
            re.search(r'[0-9]', senha) and
            re.search(r'[A-Z]', senha) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', senha))

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = re.sub(r'[^\w\s-]', '', text.lower().strip())
    return re.sub(r'[-\s]+', '-', text)