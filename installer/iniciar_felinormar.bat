@echo off
REM Taller Felinormar - Script de inicio
REM Desarrollado por: Felipe Norberto Marcelino
REM Copyright (c) 2026 Felipe Norberto Marcelino

title Taller Felinormar - Sistema de Gestion
color 0B

echo ========================================
echo   TALLER FELINORMAR v2.0
echo   Sistema de Gestion de Reparaciones
echo ========================================
echo.
echo Desarrollado por: Felipe Norberto Marcelino
echo Licencia: Trial 15 dias
echo.
echo ========================================
echo.

REM Cambiar al directorio de la aplicacion
cd /d "%~dp0"

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        echo [INFO] Asegurese de tener Python 3.11+ instalado
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
    echo.
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar si las dependencias estan instaladas
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [INFO] Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Error al instalar dependencias
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas
    echo.
)

REM Verificar si existe la base de datos
if not exist "instance\taller_felinormar.db" (
    echo [INFO] Inicializando base de datos...
    python scripts\setup_db.py
    if errorlevel 1 (
        echo [ERROR] Error al inicializar la base de datos
        pause
        exit /b 1
    )
    echo [OK] Base de datos inicializada
    echo.
)

REM Configurar variables de entorno
set FLASK_ENV=development
set FLASK_APP=wsgi:app

echo ========================================
echo   INICIANDO SERVIDOR...
echo ========================================
echo.
echo [INFO] El servidor se iniciara en:
echo        http://127.0.0.1:5000
echo.
echo [INFO] Credenciales por defecto:
echo        Usuario: admin
echo        Password: admin123
echo.
echo [IMPORTANTE] Cambie la contrasena en produccion
echo.
echo ========================================
echo.
echo Presione Ctrl+C para detener el servidor
echo.

REM Iniciar el servidor Flask
python -m flask run --host=0.0.0.0 --port=5000

REM Si el servidor se detiene
echo.
echo [INFO] Servidor detenido
pause
