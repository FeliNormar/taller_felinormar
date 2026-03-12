"""
Sistema de Gestión de Taller Felinormar
WSGI entry point para servidores de producción (Gunicorn, uWSGI, etc.)

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
import os
from app import create_app

# Determinar el entorno
env = os.environ.get('FLASK_ENV', 'production')

# Crear la aplicación
app = create_app(config_name=env)

if __name__ == '__main__':
    # Solo para desarrollo local
    app.run()
