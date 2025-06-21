from flask import Flask, render_template
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

mail = Mail()
s = None

def create_app(config_class=None):
    app = Flask(__name__)
    
    if config_class is None:
        from .config import Config
        app.config.from_object(Config)
    else:
        app.config.from_object(config_class)
    
    if not app.config.get('SECRET_KEY'):
        raise ValueError("SECRET_KEY must be set")

    mail.init_app(app)
    
    global s
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    
    # Register blueprints
    from .authentication.routes import auth_bp
    from .employee.routes import employee_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403