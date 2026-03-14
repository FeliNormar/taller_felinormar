"""
Configuraciones de la aplicación

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

# Crear carpeta instance si no existe
os.makedirs(INSTANCE_DIR, exist_ok=True)


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-felinormar-2026-cambiar-en-produccion')
    DATABASE_PATH = os.path.join(INSTANCE_DIR, 'taller_felinormar.db')
    PERMANENT_SESSION_LIFETIME = 86400  # 24 horas


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prod-key-felinormar-2026-cambiar-en-produccion')


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATABASE_PATH = os.path.join(INSTANCE_DIR, 'test.db')
