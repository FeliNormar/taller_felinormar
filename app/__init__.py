"""
Taller Felinormar - Sistema de Gestión de Reparaciones
Factory Pattern para Flask Application

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
from flask import Flask, redirect, url_for, render_template, request, flash, session
import os
import sys


def create_app(config_name='production'):
    """
    Application Factory Pattern
    
    Args:
        config_name: 'development', 'production', or 'testing'
    
    Returns:
        Flask application instance
    """
    # Detectar si estamos en .exe o desarrollo
    if getattr(sys, 'frozen', False):
        # Ejecutándose como .exe
        base_path = sys._MEIPASS
        template_folder = os.path.join(base_path, 'templates')
        static_folder = os.path.join(base_path, 'static')
    else:
        # Ejecutándose como script Python
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_folder = os.path.join(base_path, 'templates')
        static_folder = os.path.join(base_path, 'static')
    
    app = Flask(__name__, 
                template_folder=template_folder,
                static_folder=static_folder)
    
    # Cargar configuración
    if config_name == 'development':
        app.config.from_object('app.config.DevelopmentConfig')
    elif config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.ProductionConfig')
    
    # Inicializar base de datos
    from app.models.database import init_db, get_db
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
    
    # ============================================================
    # RUTA DE INSTALACIÓN INICIAL (PRIMER ARRANQUE)
    # ============================================================
    @app.route('/setup', methods=['GET', 'POST'])
    def setup():
        """
        Instalación inicial del sistema - Primer Arranque
        
        Esta ruta solo es accesible cuando no hay usuarios en la BD.
        Permite configurar el sistema por primera vez creando el usuario administrador.
        """
        from werkzeug.security import generate_password_hash
        
        # Asegurar que las tablas existan
        try:
            init_db()
        except:
            pass  # Ya están creadas
        
        # Verificar si ya hay usuarios
        conn = get_db()
        try:
            usuarios = conn.execute("SELECT COUNT(*) as count FROM usuarios").fetchone()
            
            if usuarios and usuarios['count'] > 0:
                # Ya hay usuarios, redirigir al login
                flash('El sistema ya está configurado', 'info')
                return redirect(url_for('auth.login'))
        except:
            # Tabla no existe, crearla
            init_db()
        
        if request.method == 'POST':
            nombre_taller = request.form.get('nombre_taller', '').strip()
            nombre_admin = request.form.get('nombre_admin', '').strip()
            password = request.form.get('password', '').strip()
            password_confirm = request.form.get('password_confirm', '').strip()
            
            # ============================================================
            # VALIDACIONES PROFESIONALES
            # ============================================================
            
            # Validar campos obligatorios
            if not nombre_taller:
                flash('El nombre del taller es obligatorio', 'error')
                return render_template('setup.html')
            
            if not nombre_admin:
                flash('El nombre del administrador es obligatorio', 'error')
                return render_template('setup.html')
            
            if not password:
                flash('La contraseña es obligatoria', 'error')
                return render_template('setup.html')
            
            # Validar confirmación de contraseña
            if password != password_confirm:
                flash('Las contraseñas no coinciden', 'error')
                return render_template('setup.html')
            
            # Validar longitud mínima de contraseña
            if len(password) < 6:
                flash('La contraseña debe tener al menos 6 caracteres', 'error')
                return render_template('setup.html')
            
            try:
                # Verificar que no exista el usuario (por seguridad)
                existing = conn.execute(
                    "SELECT id FROM usuarios WHERE usuario=?",
                    (nombre_admin,)
                ).fetchone()
                
                if existing:
                    flash('El nombre de usuario ya existe', 'error')
                    return render_template('setup.html')
                
                # Crear usuario administrador con contraseña encriptada
                conn.execute(
                    "INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)",
                    (nombre_admin, generate_password_hash(password), 'admin')
                )
                
                # Crear configuración del taller (si existe la tabla - versión PRO)
                try:
                    conn.execute('''
                        INSERT OR REPLACE INTO configuracion 
                        (id, nombre_taller, nombre_propietario, ubicacion)
                        VALUES (1, ?, ?, 'Ubicación del taller')
                    ''', (nombre_taller, nombre_admin))
                except:
                    pass  # Tabla configuracion no existe en versión básica
                
                conn.commit()
                
                flash('¡Sistema configurado correctamente! Inicia sesión con tus credenciales', 'success')
                return redirect(url_for('auth.login'))
                
            except Exception as e:
                conn.rollback()
                flash(f'Error al configurar el sistema: {str(e)}', 'error')
                return render_template('setup.html')
        
        return render_template('setup.html')
    
    # ============================================================
    # MIDDLEWARE DE INICIALIZACIÓN
    # ============================================================
    @app.before_request
    def check_setup():
        """
        Middleware que verifica si el sistema necesita configuración inicial.
        Solo redirige a /setup si la tabla usuarios está vacía.
        """
        # Rutas que nunca requieren verificación
        excluded_routes = {
            'setup', 'static', 'auth.login', 'auth.logout',
            'ordenes.status_publico'
        }

        if request.endpoint in excluded_routes or request.endpoint is None:
            return None

        if request.path.startswith('/static/'):
            return None

        # Verificar si hay usuarios — si falla, no interrumpir
        try:
            conn = get_db()
            count = conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
            if count == 0:
                return redirect(url_for('setup'))
        except Exception:
            # Si la tabla no existe aún, redirigir a setup
            return redirect(url_for('setup'))

        return None
    
    return app
