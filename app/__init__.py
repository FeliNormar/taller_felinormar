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
        try:
            init_db()
        except Exception as e:
            print(f"ERROR init_db: {e}", file=sys.stderr)
            raise
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.ordenes import ordenes_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.reparaciones import reparaciones_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.pantallas import pantallas_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(ordenes_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(reparaciones_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pantallas_bp)
    
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
            email_admin = request.form.get('email_admin', '').strip().lower()
            
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
                    "INSERT INTO usuarios (usuario, password, rol, email) VALUES (?, ?, ?, ?)",
                    (nombre_admin, generate_password_hash(password), 'admin', email_admin)
                )
                
                # Crear configuración del taller (si existe la tabla - versión PRO)
                try:
                    from app.models.database import USE_POSTGRES
                    if USE_POSTGRES:
                        conn.execute('''
                            INSERT INTO configuracion (id, nombre_taller, nombre_propietario, email, telefono, calle, colonia, municipio, estado, cp, completado)
                            VALUES (1, %s, %s, '', '', '', '', '', '', '', 0)
                            ON CONFLICT (id) DO NOTHING
                        ''', (nombre_taller, nombre_admin))
                    else:
                        conn.execute('''
                            INSERT OR REPLACE INTO configuracion 
                            (id, nombre_taller, nombre_propietario, ubicacion)
                            VALUES (1, ?, ?, 'Ubicación del taller')
                        ''', (nombre_taller, nombre_admin))
                except:
                    pass  # Tabla configuracion no existe en versión básica
                
                conn.commit()
                
                flash('¡Sistema configurado correctamente! Completa los datos de tu taller.', 'success')
                return redirect(url_for('onboarding'))
                
            except Exception as e:
                conn.rollback()
                flash(f'Error al configurar el sistema: {str(e)}', 'error')
                return render_template('setup.html')
        
        return render_template('setup.html')
    
    # ============================================================
    # ONBOARDING — Datos del taller (se pide una sola vez)
    # ============================================================
    @app.route('/onboarding', methods=['GET', 'POST'])
    def onboarding():
        """Formulario de datos del taller — se muestra una sola vez tras el setup"""
        conn = get_db()

        # Si ya está completado, ir al login
        cfg = conn.execute("SELECT completado FROM configuracion WHERE id=1").fetchone()
        if cfg and cfg['completado'] == 1:
            return redirect(url_for('auth.login'))

        if request.method == 'POST':
            nombre_taller     = request.form.get('nombre_taller', '').strip()
            nombre_propietario = request.form.get('nombre_propietario', '').strip()
            email             = request.form.get('email', '').strip()
            telefono          = request.form.get('telefono', '').strip()
            calle             = request.form.get('calle', '').strip()
            colonia           = request.form.get('colonia', '').strip()
            municipio         = request.form.get('municipio', '').strip()
            estado            = request.form.get('estado', '').strip()
            cp                = request.form.get('cp', '').strip()

            if not all([nombre_taller, nombre_propietario, calle, municipio, estado, cp]):
                flash('Completa todos los campos obligatorios.', 'error')
                return render_template('onboarding.html')

            from app.models.database import USE_POSTGRES
            if USE_POSTGRES:
                conn.execute('''
                    INSERT INTO configuracion
                    (id, nombre_taller, nombre_propietario, email, telefono,
                     calle, colonia, municipio, estado, cp, completado)
                    VALUES (1, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                    ON CONFLICT (id) DO UPDATE SET
                        nombre_taller=%s, nombre_propietario=%s, email=%s,
                        telefono=%s, calle=%s, colonia=%s, municipio=%s,
                        estado=%s, cp=%s, completado=1
                ''', (nombre_taller, nombre_propietario, email, telefono,
                      calle, colonia, municipio, estado, cp,
                      nombre_taller, nombre_propietario, email, telefono,
                      calle, colonia, municipio, estado, cp))
            else:
                conn.execute('''
                    INSERT OR REPLACE INTO configuracion
                    (id, nombre_taller, nombre_propietario, email, telefono,
                     calle, colonia, municipio, estado, cp, completado)
                    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                ''', (nombre_taller, nombre_propietario, email, telefono,
                      calle, colonia, municipio, estado, cp))
            conn.commit()

            flash('¡Datos del taller guardados! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))

        return render_template('onboarding.html')

    # ============================================================
    # HEADERS DE SEGURIDAD HTTP
    # ============================================================
    @app.after_request
    def security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        # Solo en producción activar HSTS
        if not app.debug:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

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
            'auth.forgot_password', 'auth.reset_password',
            'ordenes.status_publico', 'onboarding'
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
            # Verificar si el onboarding está completo
            cfg = conn.execute(
                "SELECT completado FROM configuracion WHERE id=1"
            ).fetchone()
            if not cfg or cfg['completado'] == 0:
                return redirect(url_for('onboarding'))
        except Exception:
            return redirect(url_for('setup'))

        return None
    
    return app
