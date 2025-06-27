from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import current_app
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()