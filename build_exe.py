"""
Script para generar ejecutable .exe de Taller Felinormar
Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
import PyInstaller.__main__
import os
import shutil

print("=" * 60)
print("  TALLER FELINORMAR - GENERADOR DE EJECUTABLE")
print("=" * 60)
print()

# Limpiar builds anteriores
if os.path.exists('build'):
    print("[INFO] Limpiando carpeta build...")
    shutil.rmtree('build')
if os.path.exists('dist'):
    print("[INFO] Limpiando carpeta dist...")
    shutil.rmtree('dist')

print("[INFO] Generando ejecutable...")
print()

# Configuración de PyInstaller
PyInstaller.__main__.run([
    'wsgi.py',                          # Archivo principal
    '--name=TallerFelinormar',          # Nombre del ejecutable
    '--onefile',                        # Un solo archivo .exe
    '--windowed',                       # Sin consola (GUI)
    '--add-data=templates;templates',   # Incluir templates
    '--add-data=static;static',         # Incluir static
    '--add-data=app;app',               # Incluir app
    '--add-data=docs;docs',             # Incluir docs
    '--add-data=LICENSE;.',             # Incluir licencia
    '--add-data=README.md;.',           # Incluir readme
    '--hidden-import=flask',
    '--hidden-import=werkzeug',
    '--hidden-import=jinja2',
    '--hidden-import=click',
    '--hidden-import=itsdangerous',
    '--hidden-import=markupsafe',
    '--collect-all=flask',
    '--collect-all=werkzeug',
    '--noconfirm',                      # No pedir confirmación
    '--clean',                          # Limpiar cache
])

print()
print("=" * 60)
print("  EJECUTABLE GENERADO EXITOSAMENTE")
print("=" * 60)
print()
print("Ubicación: dist/TallerFelinormar.exe")
print()
