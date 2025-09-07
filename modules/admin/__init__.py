from .routes import bp as admin_bp
from flask import Blueprint
#from .models import init_admin_models - a ideia era ter um banco de dados para o admin mas 
from .routes import bp
def init_admin(app):
    from . import routes
    #Inicializa o módulo admin"""
    app.register_blueprint(bp)
    
    # Inicializa modelos específicos
   ##    init_admin_models()