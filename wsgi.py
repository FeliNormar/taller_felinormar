"""
Sistema de Gestión de Taller Felinormar
WSGI entry point para servidores de producción (Gunicorn, uWSGI, etc.)

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
import os
import sys
from dotenv import load_dotenv
load_dotenv()
from app import create_app

# Para PyInstaller: agregar rutas de recursos empaquetados
if getattr(sys, 'frozen', False):
    # Ejecutándose como .exe
    application_path = sys._MEIPASS
else:
    # Ejecutándose como script Python normal
    application_path = os.path.dirname(os.path.abspath(__file__))

# Determinar el entorno
env = os.environ.get('FLASK_ENV', 'production')

# Crear la aplicación
app = create_app(config_name=env)

if __name__ == '__main__':
    # Solo para desarrollo local o ejecutable
    import webbrowser
    import threading
    
    def abrir_navegador():
        """Abrir navegador automáticamente después de 1.5 segundos"""
        import time
        time.sleep(1.5)
        webbrowser.open('http://127.0.0.1:5000')
    
    print("=" * 60)
    print("  TALLER FELINORMAR v2.0")
    print("  Sistema de Gestión de Reparaciones")
    print("=" * 60)
    print()
    print("Desarrollado por: Felipe Norberto Marcelino")
    print("Licencia: Trial 15 días")
    print()
    print("=" * 60)
    print()
    print("Servidor iniciado en: http://127.0.0.1:5000")
    print()
    print("Credenciales por defecto:")
    print("  Usuario: admin")
    print("  Password: admin123")
    print()
    print("IMPORTANTE: Cambie la contraseña en producción")
    print()
    print("=" * 60)
    print()
    print("Presione Ctrl+C para detener el servidor")
    print()
    
    # Abrir navegador en un hilo separado
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    # Iniciar servidor
    app.run(host='0.0.0.0', port=5000, debug=False)
