"""
Taller Felinormar - Sistema de Gestión de Reparaciones
Factory Pattern para Flask Application
"""
from flask import Flask
import os


def create_app(config_name='production'):
    """
    Application Factory Pattern
    
    Args:
        config_name: 'development', 'production', or 'testing'
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Cargar configuración
    if config_name == 'development':
        app.config.from_object('app.config.DevelopmentConfig')
    elif config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.ProductionConfig')
    
    # Inicializar base de datos
    from app.models.database import init_db
    with app.app_context():
        init_db()
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.ordenes import ordenes_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.reparaciones import reparaciones_bp
    from app.routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(ordenes_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(reparaciones_bp)
    app.register_blueprint(dashboard_bp)
    
    return app
