from flask import Flask
from .extensions import db, login_manager

def init_core(app):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    
    
    return app