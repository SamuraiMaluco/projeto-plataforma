from .routes import bp as payments_bp

def init_payments(app):
    """Inicializa o módulo de pagamentos"""
    app.register_blueprint(payments_bp, url_prefix='/payments')