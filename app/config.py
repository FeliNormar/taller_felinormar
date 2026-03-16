"""
Configuraciones de la aplicación

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)


class BaseConfig:
    # ── Sesión ────────────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY')  # OBLIGATORIO en producción
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_HTTPONLY  = True   # JS no puede leer la cookie
    SESSION_COOKIE_SAMESITE  = 'Lax' # Protección CSRF básica
    SESSION_COOKIE_SECURE    = False  # Se sobreescribe en Producción

    # ── Base de datos ─────────────────────────────────────────
    DATABASE_PATH = os.environ.get(
        'DATABASE_PATH',
        os.path.join(INSTANCE_DIR, 'taller_felinormar.db')
    )

    # ── Uploads ───────────────────────────────────────────────
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB máximo por archivo

    # ── Email (recuperación de contraseña) ────────────────────
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # App password de Gmail
    RESEND_API_KEY = os.environ.get('RESEND_API_KEY')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-key-no-usar-en-produccion')
    SESSION_COOKIE_SECURE = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True   # Solo HTTPS
    # SECRET_KEY DEBE venir de variable de entorno — sin fallback
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'test-key'
    DATABASE_PATH = os.path.join(INSTANCE_DIR, 'test.db')
