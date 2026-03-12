"""
WSGI entry point para servidores de producción (Gunicorn, uWSGI, etc.)
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
